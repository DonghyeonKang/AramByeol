import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './contexts/ThemeContext';
import { AuthProvider } from './contexts/AuthContext';
import { Layout } from './components/templates/Layout/Layout';
import { Home } from './pages/Home/Home';
import { Login } from './pages/Login/Login';
import { SignUp } from './pages/SignUp/SignUp';
import { Weekly } from './pages/Weekly/Weekly';
import { Profile } from './pages/Profile/Profile';
import { Settings } from './pages/Settings/Settings';
import { Reviews } from './pages/Reviews/Reviews';
import { Roommate } from './pages/Roommate/Roommate';
import { Chat } from './pages/Chat/Chat';
import './styles/theme.css';
import './App.css';

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <Router>
          <Routes>
            <Route element={<Layout />}>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<SignUp />} />
              <Route path="/weekly" element={<Weekly />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="/settings" element={<Settings />} />
              <Route path="/reviews" element={<Reviews />} />
              <Route path="/roommate" element={<Roommate />} />
              <Route path="/chat" element={<Chat />} />
            </Route>
          </Routes>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
