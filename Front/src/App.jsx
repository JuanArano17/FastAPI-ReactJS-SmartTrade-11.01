import './App.css';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'
import HomePage from './pages/HomePage';
import RegisterSelectionPage from './pages/RegisterSelectionPage';
import LoginPage from './pages/LoginPage';
import ForgotPasswordPage from './pages/ForgotPasswordPage';
import ProductDetailPage from './components/ProductDetailPage';
import CatalogPage from './pages/CatalogPage';


function App() {
  return (
    <div className="App">
      <Router>
        <Switch>
          <Route path="/home" component={HomePage} />
          <Route path="/login" component={LoginPage} />
          <Route path="/details" component={ProductDetailPage} />
          <Route path="/catalog" component={CatalogPage} />
          <Route path="/forgotPassword" component={ForgotPasswordPage} />
          <Route path="/register" component={RegisterSelectionPage} />
          <Route exact path="/" component={HomePage} />
        </Switch>
      </Router>
    </div>
  );
}

export default App;
