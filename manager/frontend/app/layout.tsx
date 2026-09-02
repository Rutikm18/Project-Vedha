import type { Metadata } from "next";
import "./globals.css";
import "../styles/console-tokens.css";
import { ToastProvider } from "../components/ToastProvider";
import { ThemeProvider } from "../components/ThemeProvider";
import { QueryProvider } from "../components/QueryProvider";
import { AssistantProvider } from "../components/assistant/AssistantProvider";

export const metadata: Metadata = {
  title: "Vedha — Network vulnerability operations",
  description: "Evidence-led network vulnerability assessment and remediation operations",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        {/* Anti-FOUC: apply stored theme before first paint + enable smooth theme transitions */}
        <script
          dangerouslySetInnerHTML={{
            __html: `(function(){try{var s=localStorage.getItem('vedha-theme');var p=window.matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light';document.documentElement.setAttribute('data-theme',s||p);}catch(e){document.documentElement.setAttribute('data-theme','light');}
setTimeout(function(){document.documentElement.classList.add('theme-transition')},400);})();`,
          }}
        />
      </head>
      <body className="antialiased" suppressHydrationWarning>
        <QueryProvider>
          <ThemeProvider>
            <ToastProvider>
              <AssistantProvider>{children}</AssistantProvider>
            </ToastProvider>
          </ThemeProvider>
        </QueryProvider>
      </body>
    </html>
  );
}
