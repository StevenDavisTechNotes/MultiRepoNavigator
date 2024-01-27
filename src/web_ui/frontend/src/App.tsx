import {
  Route,
  BrowserRouter as Router,
  Routes,
} from "react-router-dom";
import './App.css';
import Navbar from "./components/Navbar";
import Home from "./pages";
import About from "./pages/about";
import NavigatorPage from "./pages/navigator";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route
          path="/navigator"
          element={<NavigatorPage />}
        />
      </Routes>
    </Router>
  );
}

export default App;
