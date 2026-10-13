import { Command }                    from 'commander';
import * as readline                  from 'readline';
import { saveSession, serverUrl, loadSession, loginWithPassword, LoginError } from '../auth';

function prompt(question: string): Promise<string> {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer.trim());
    });
  });
}

function promptSilent(question: string): Promise<string> {
  return new Promise((resolve) => {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    process.stdout.write(question);
    // Disable echo while typing
    (process.stdin as NodeJS.ReadStream).setRawMode?.(true);
    let input = '';
    process.stdin.resume();
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', function handler(char: string) {
      if (char === '\r' || char === '\n') {
        process.stdin.removeListener('data', handler);
        (process.stdin as NodeJS.ReadStream).setRawMode?.(false);
        process.stdout.write('\n');
        rl.close();
        resolve(input);
      } else if (char === '\x7f' || char === '\b') {
        if (input.length > 0) {
          input = input.slice(0, -1);
          process.stdout.write('\b \b');
        }
      } else if (char === '\x03') {
        process.exit();
      } else {
        input += char;
        process.stdout.write('*');
      }
    });
  });
}

export function buildLoginCommand(): Command {
  return new Command('login')
    .description('Sign in to VEDHA with your email and password')
    .action(async () => {
      const existing = loadSession();
      if (existing) {
        process.stdout.write(`\x1b[33mAlready logged in as \x1b[1m${existing.email}\x1b[0m\n`);
        process.stdout.write(`Run \x1b[1mvedha logout\x1b[0m first to switch accounts.\n`);
        return;
      }

      const server = serverUrl();
      process.stdout.write(`\x1b[1;36mVEDHA\x1b[0m  ${server}\n\n`);

      const email = await prompt('Email: ');
      if (!email || !email.includes('@')) {
        process.stderr.write('\x1b[1;31m[ERR]\x1b[0m Invalid email\n');
        process.exit(1);
      }
      const password = await promptSilent('Password: ');
      if (!password) {
        process.stderr.write('\x1b[1;31m[ERR]\x1b[0m No password entered\n');
        process.exit(1);
      }

      process.stdout.write('\x1b[2mSigning in…\x1b[0m\n');
      try {
        const session = await loginWithPassword(server, email, password, () => prompt('Authenticator code (or recovery code): '));
        saveSession(session);
        process.stdout.write(`\n\x1b[1;32m✓\x1b[0m Authenticated as \x1b[1m${session.email}\x1b[0m`);
        process.stdout.write(session.role === 'admin' ? ' \x1b[36m[admin]\x1b[0m' : '');
        process.stdout.write('\n');
      } catch (e) {
        process.stderr.write(`\x1b[1;31m[ERR]\x1b[0m ${e instanceof LoginError ? e.message : 'Authentication failed'}\n`);
        process.exit(1);
      }
    });
}
