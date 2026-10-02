import { Command }              from 'commander';
import { clearSession, loadSession, revokeSessionToken } from '../auth';

export function buildLogoutCommand(): Command {
  return new Command('logout')
    .description('Clear your VEDHA session')
    .action(async () => {
      const s = loadSession();
      if (!s) {
        process.stdout.write('Not logged in.\n');
        return;
      }
      await revokeSessionToken(s);
      clearSession();
      process.stdout.write(`\x1b[1;32m✓\x1b[0m Logged out (${s.email})\n`);
    });
}
