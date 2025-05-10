import { ReactNode } from 'react';
import './MainLayout.css';

interface MainLayoutProps {
  children: ReactNode;
}

export const MainLayout = ({ children }: MainLayoutProps) => {
  return (
    <div className="main-layout">
      <header className="header">
        <nav>{/* Navigation components */}</nav>
      </header>
      <main className="main-content">
        {children}
      </main>
      <footer className="footer">
        {/* Footer content */}
      </footer>
    </div>
  );
}; 