Vedha Agent - Windows quick start
=================================

1) Unzip this folder anywhere (for example  C:\vedha-agent ).

2) TEST IT  (see it connect - no admin needed):
     Double-click  run.cmd
   A window shows:  enrolled -> WebSocket connected -> waiting for jobs.
   Close the window to stop.

3) RUN IT PERMANENTLY  (survives reboot - one-time admin prompt):
     Right-click  install.cmd  ->  Run as administrator
   The agent is registered as a background task named "VedhaAgent" and starts now.

To remove:
     Right-click  uninstall.cmd  ->  Run as administrator

Easier next time: your Vedha portal (Fleet -> Add agent) gives a single command that downloads,
verifies and installs the agent for you. Use it instead of this ZIP when you can.

The folder C:\ProgramData\vedha-agent is readable by Administrators and SYSTEM only (it holds the
agent's identity key). run.cmd after a permanent install therefore needs an administrator prompt.

Firewall (only if outbound is restricted):
   Allow this PC to reach   your Vedha manager address (shown in the portal)  TCP 443   (OUTBOUND only).
   The agent never opens an inbound port.

Logs:      C:\ProgramData\vedha-agent\logs\agent.log
Identity:  C:\ProgramData\vedha-agent\state.json   (do not share)

Note: your antivirus / EDR may flag a network scanner. If so, allow
"vedha-agent.exe" with your security team before installing.
