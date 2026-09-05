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

Firewall (only if outbound is restricted):
   Allow this PC to reach   13.127.147.205  TCP 18080   (OUTBOUND only).
   The agent never opens an inbound port.

Logs:      C:\ProgramData\vedha-agent\logs\agent.log
Identity:  C:\ProgramData\vedha-agent\state.json   (do not share)

Note: your antivirus / EDR may flag a network scanner. If so, allow
"vedha-agent.exe" with your security team before installing.
