import { Outlet } from 'react-router-dom';
import { Header } from '../../organisms/Header/Header';
import { Footer } from '../../organisms/Footer/Footer';
import './Layout.css';

export const Layout = () => {
  return (
    <div className="layout">
      <Header />
      <main className="main">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}; 