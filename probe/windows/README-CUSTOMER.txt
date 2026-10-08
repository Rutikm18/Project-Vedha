Vedha agent - Windows installation
==================================

You need
  - Windows 10 or Windows Server 2016 or newer (64-bit), and administrator rights.
  - Outbound access to your Vedha manager on TCP 443 (the installer checks this first).
  - The one-time INSTALL TOKEN your Vedha contact sent you (it starts with vet_ and works once).
  Nothing else: no Python, no downloads. Everything the agent needs is in this package.

Install - one command
  1. Check the file you received. In PowerShell:
         Get-FileHash .\vedha-agent-win.zip -Algorithm SHA256
     The value must match the one your Vedha contact gave you separately (phone or chat).
  2. Unzip it, for example to C:\vedha-install, and open a Command Prompt or PowerShell there.
  3. Run:
         install.cmd -Token vet_XXXXXXXX
     Windows asks you to confirm administrator access. The installer then checks your
     computer and your connection to the manager, installs, connects, and finishes with
     either SUCCESS or the exact thing to fix. Nothing is installed if the checks fail.

  Behind a web proxy:      install.cmd -Token vet_XXXXXXXX -Proxy http://proxy:3128
  HTTPS is inspected:      install.cmd -Token vet_XXXXXXXX -CaBundle C:\certs\company-root.pem
  Scan a different network: install.cmd -Repair -Scope 10.0.5.0/24
  (By default the agent may scan only the network this computer is on.)

If something goes wrong
  - Read the message: it says what was found and what to change. Fix it and run the same command again.
  - From an Administrator prompt you can check the agent at any time:
         "C:\Program Files\Vedha Agent\vedha-agent.exe" status      what it is doing now
         "C:\Program Files\Vedha Agent\vedha-agent.exe" doctor      checks the connection, explains problems
  - To get help, create a file for Vedha support and email it to your Vedha contact:
         "C:\Program Files\Vedha Agent\vedha-agent.exe" support-bundle
     It contains no passwords, tokens or keys. It does contain host names and IP addresses
     (add --mask-ips to hide them). Nothing is sent automatically.
  - Antivirus or endpoint protection blocked something? Give ALLOWLIST.txt to your security team.

Installing from your Vedha portal instead?
  Fleet -> Add agent -> Windows gives a single command that downloads this same package, checks the
  signed release (and, when the release is Authenticode-signed, the signature on vedha-agent.exe) and
  runs the installer below for you. You do not need to unzip anything. The agent is the same either way.
  To remove an agent installed that way, from an Administrator prompt:
      C:\ProgramData\vedha-agent\tools\uninstall.cmd   (add -Purge to also delete its identity and logs)

Other commands
  install.cmd -Repair            re-apply the installation and re-check it (keeps the agent's identity)
  install.cmd -Uninstall         remove the agent  (add -Purge to also delete its identity and logs)
  run.cmd                        run the agent in this window to see it connect (no administrator rights needed;
                                 close the window to stop)

Where things are
  Program : C:\Program Files\Vedha Agent\
  Data    : C:\ProgramData\vedha-agent\   settings, identity (do not share), logs\agent.log, logs\install-*.log
  Runs as : scheduled task "VedhaAgent" (SYSTEM), started at boot, restarted if it stops

The agent only connects OUT to your Vedha manager (TCP 443). It opens no inbound port.
It does not change your firewall, proxy, antivirus or certificate settings.
