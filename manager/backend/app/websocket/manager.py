"""
WebSocket manager for real-time graph updates, agent push, and live collaboration.

Provides:
- Broadcasting graph updates to connected clients
- Real-time node position updates during force simulation
- Live collaboration features (multiple users viewing same graph)
- Heartbeat/ping-pong for connection health monitoring
- Agent push: direct WebSocket job dispatch to probes
"""
from __future__ import annotations

import asyncio
import json
from collections import defaultdict
from typing import Dict, Optional, Set
from datetime import datetime, timezone

from fastapi import WebSocket, WebSocketDisconnect
import structlog

logger = structlog.get_logger()


class ConnectionManager:
    """Manages WebSocket connections with room-based broadcasting."""

    def __init__(self):
        self._rooms: Dict[str, Set[WebSocket]] = defaultdict(set)
        self._connections: Dict[WebSocket, str] = {}
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, room_id: str):
        """Accept connection and add to room."""
        await websocket.accept()
        async with self._lock:
            self._rooms[room_id].add(websocket)
            self._connections[websocket] = room_id
        logger.info("websocket.client_connected", room=room_id)

    async def disconnect(self, websocket: WebSocket):
        """Remove connection from room."""
        async with self._lock:
            room_id = self._connections.pop(websocket, None)
            if room_id and websocket in self._rooms[room_id]:
                self._rooms[room_id].discard(websocket)
        logger.info("websocket.client_disconnected", room=room_id)

    async def broadcast(self, room_id: str, message: dict, exclude: Optional[WebSocket] = None):
        """Broadcast message to all connections in a room."""
        if room_id not in self._rooms:
            return

        dead_connections = []
        for websocket in self._rooms[room_id]:
            if websocket == exclude:
                continue
            try:
                await websocket.send_json(message)
            except Exception:
                dead_connections.append(websocket)

        for ws in dead_connections:
            await self.disconnect(ws)

    async def send_personal(self, websocket: WebSocket, message: dict):
        """Send message to a specific connection."""
        try:
            await websocket.send_json(message)
        except Exception:
            await self.disconnect(websocket)

    async def get_room_clients(self, room_id: str) -> int:
        """Get number of connected clients in a room."""
        return len(self._rooms.get(room_id, set()))


class AgentConnectionManager:
    """Tracks WebSocket connections from probes/agents for direct job push.

    Each connected agent is keyed by its agent_id (UUID string). Only one
    WebSocket connection per agent is allowed — a new connection displaces
    the old one (which gets closed with a "displaced" reason).
    """

    def __init__(self):
        self._agents: Dict[str, WebSocket] = {}        # agent_id → websocket
        self._agent_status: Dict[str, str] = {}        # agent_id → "online"|"busy"
        self._agent_job: Dict[str, str | None] = {}    # agent_id → current_job_id
        self._agent_tenant: Dict[str, str] = {}        # agent_id → tenant_id
        self._agent_features: Dict[str, Set[str]] = {}  # agent_id → protocol features
        self._agent_last_hb: Dict[str, datetime] = {}   # agent_id → last heartbeat
        self._lock = asyncio.Lock()

    # ── Registration ──────────────────────────────────────────────────────────

    async def register(self, agent_id: str, tenant_id: str,
                       websocket: WebSocket) -> None:
        """Register an agent's WebSocket connection.

        If the agent already has a connection, the old one is displaced
        (disconnected gracefully) before the new one is registered. This
        ensures a single probe doesn't accidentally maintain two connections.
        """
        async with self._lock:
            old = self._agents.get(agent_id)
            if old is not None and old is not websocket:
                try:
                    await old.send_json({
                        "type": "displaced",
                        "message": "A newer connection displaced this one.",
                    })
                    await old.close(code=1000)
                except Exception:
                    pass
            self._agents[agent_id] = websocket
            self._agent_status[agent_id] = "online"
            self._agent_job[agent_id] = None
            self._agent_tenant[agent_id] = tenant_id
            self._agent_features[agent_id] = set()
            self._agent_last_hb[agent_id] = datetime.now(timezone.utc)
        logger.info("agent.ws.connected", agent_id=agent_id, tenant_id=tenant_id)

    async def unregister(
        self,
        agent_id: str,
        websocket: WebSocket | None = None,
    ) -> bool:
        """Remove the current registration, optionally only for one socket.

        Returns True only when a live registration was removed. A displaced
        handler must pass its socket so it cannot unregister a newer reconnect.
        """
        async with self._lock:
            current = self._agents.get(agent_id)
            if current is None or (
                websocket is not None and current is not websocket
            ):
                return False
            self._agents.pop(agent_id, None)
            self._agent_status.pop(agent_id, None)
            self._agent_job.pop(agent_id, None)
            self._agent_tenant.pop(agent_id, None)
            self._agent_features.pop(agent_id, None)
            self._agent_last_hb.pop(agent_id, None)
        logger.info("agent.ws.disconnected", agent_id=agent_id)
        return True

    # ── Heartbeat ─────────────────────────────────────────────────────────────

    async def record_heartbeat(self, agent_id: str, status: str,
                               current_job_id: str | None = None) -> None:
        """Record a heartbeat from an agent."""
        async with self._lock:
            if agent_id in self._agent_last_hb:
                self._agent_last_hb[agent_id] = datetime.now(timezone.utc)
                self._agent_status[agent_id] = status
                if current_job_id is not None:
                    self._agent_job[agent_id] = current_job_id
                elif status == "online":
                    self._agent_job[agent_id] = None

    async def record_features(
        self,
        agent_id: str,
        features: list[str] | set[str] | tuple[str, ...],
    ) -> None:
        """Record transport features explicitly advertised by a connected probe."""
        async with self._lock:
            if agent_id in self._agents:
                self._agent_features[agent_id] = {
                    str(feature) for feature in features if feature
                }

    # ── Push job ──────────────────────────────────────────────────────────────

    async def push_job(
        self,
        agent_id: str,
        job: dict,
        required_feature: str | None = None,
    ) -> bool:
        """Push a job to a specific agent over WebSocket.

        Returns True if the job was sent successfully, False if the agent
        is not connected or the send failed.
        """
        async with self._lock:
            ws = self._agents.get(agent_id)
            status = self._agent_status.get(agent_id, "offline")
            features = self._agent_features.get(agent_id, set())
        if (
            ws is None
            or status not in ("online",)
            or (required_feature is not None and required_feature not in features)
        ):
            return False
        try:
            await ws.send_json({"type": "job_push", "job": job})
            return True
        except Exception:
            await self.unregister(agent_id, ws)
            return False

    async def push_job_to_first_online(
        self,
        job: dict,
        tenant_id: str,
        required_feature: str | None = None,
    ) -> str | None:
        """Push a job to the first online agent in the requested tenant.

        Returns the agent_id that received the job, or None if no agent
        was available.
        """
        for agent_id in self.online_agents_for_tenant(
            tenant_id,
            required_feature=required_feature,
        ):
            if await self.push_job(
                agent_id,
                job,
                required_feature=required_feature,
            ):
                return agent_id
        return None

    # ── Queries ───────────────────────────────────────────────────────────────

    def is_connected(self, agent_id: str) -> bool:
        """Check if a specific agent is connected."""
        return agent_id in self._agents

    def is_online(self, agent_id: str) -> bool:
        """Check if a specific agent is online (connected + not busy)."""
        return self._agent_status.get(agent_id) in ("online",)

    @property
    def connected_agents(self) -> list[str]:
        """Return a snapshot of all connected agent IDs."""
        return list(self._agents.keys())

    @property
    def online_agents(self) -> list[str]:
        """Return agent IDs whose status is 'online' (idle, ready for job)."""
        return [aid for aid, st in self._agent_status.items() if st == "online"]

    def online_agents_for_tenant(
        self,
        tenant_id: str,
        required_feature: str | None = None,
    ) -> list[str]:
        """Return idle connected agents belonging to exactly one tenant."""
        tenant = str(tenant_id)
        return [
            agent_id
            for agent_id, status in self._agent_status.items()
            if status == "online"
            and self._agent_tenant.get(agent_id) == tenant
            and agent_id in self._agents
            and (
                required_feature is None
                or required_feature in self._agent_features.get(agent_id, set())
            )
        ]

    @property
    def connected_count(self) -> int:
        return len(self._agents)

    def get_agent_status(self, agent_id: str) -> str:
        """Return 'online', 'busy', or 'offline'."""
        return self._agent_status.get(agent_id, "offline")

    def agent_stale_after(self, seconds: float) -> list[str]:
        """Return agent_ids whose last heartbeat is older than `seconds`.

        These agents should be marked as stale / disconnected.
        """
        cutoff = datetime.now(timezone.utc)
        stale = []
        for aid, last_hb in list(self._agent_last_hb.items()):
            if (cutoff - last_hb).total_seconds() > seconds:
                stale.append(aid)
        return stale


# Global singleton — shared across the application.
agent_ws_manager = AgentConnectionManager()


class GraphWebSocketManager:
    """High-level manager for graph-specific WebSocket operations."""

    def __init__(self):
        self.manager = ConnectionManager()
        self._graph_states: Dict[str, dict] = {}

    async def handle_client(self, websocket: WebSocket, engagement_id: str):
        """Handle a new WebSocket client connection."""
        room_id = f"graph:{engagement_id}"
        await self.manager.connect(websocket, room_id)

        try:
            while True:
                data = await websocket.receive_text()
                try:
                    message = json.loads(data)
                    await self._handle_message(websocket, room_id, message)
                except json.JSONDecodeError:
                    await self.manager.send_personal(websocket, {
                        "type": "error",
                        "message": "Invalid JSON",
                        "timestamp": datetime.utcnow().isoformat(),
                    })
        except WebSocketDisconnect:
            await self.manager.disconnect(websocket)

    async def _handle_message(self, websocket: WebSocket, room_id: str, message: dict):
        """Handle incoming WebSocket messages."""
        msg_type = message.get("type")

        if msg_type == "ping":
            await self.manager.send_personal(websocket, {
                "type": "pong",
                "timestamp": datetime.utcnow().isoformat(),
            })

        elif msg_type == "graph.update":
            await self.manager.broadcast(room_id, {
                "type": "graph.updated",
                "data": message.get("data"),
                "timestamp": datetime.utcnow().isoformat(),
            }, exclude=websocket)

        elif msg_type == "graph.subscribe":
            await self.manager.send_personal(websocket, {
                "type": "graph.subscribed",
                "timestamp": datetime.utcnow().isoformat(),
            })

    async def broadcast_graph_update(self, engagement_id: str, graph_data: dict):
        """Broadcast graph data update to all subscribers."""
        room_id = f"graph:{engagement_id}"
        await self.manager.broadcast(room_id, {
            "type": "graph.data",
            "data": graph_data,
            "timestamp": datetime.utcnow().isoformat(),
        })

    async def broadcast_node_update(self, engagement_id: str, node_id: str, node_data: dict):
        """Broadcast a single node update."""
        room_id = f"graph:{engagement_id}"
        await self.manager.broadcast(room_id, {
            "type": "graph.node.updated",
            "node_id": node_id,
            "data": node_data,
            "timestamp": datetime.utcnow().isoformat(),
        })

    async def broadcast_layout_update(self, engagement_id: str, layout_type: str):
        """Broadcast layout change to all subscribers."""
        room_id = f"graph:{engagement_id}"
        await self.manager.broadcast(room_id, {
            "type": "graph.layout.changed",
            "layout": layout_type,
            "timestamp": datetime.utcnow().isoformat(),
        })
