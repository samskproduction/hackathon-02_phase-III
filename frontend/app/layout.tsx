import './globals.css';
import { Inter } from 'next/font/google';
import { ThemeProvider } from '@/providers/theme-provider';
import { BetterAuthProvider } from '@/providers/better-auth-provider';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'Todo App',
  description: 'A modern, premium todo application',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <BetterAuthProvider>
          <ThemeProvider>
            {children}
          </ThemeProvider>
        </BetterAuthProvider>
      </body>
    </html>
  );
}