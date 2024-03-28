import './App.css';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'
import HomePage from './pages/HomePage';
import RegisterSelectionPage from './pages/RegisterSelectionPage';
import RegisterSellerPage from './pages/RegisterSellerPage';
import RegisterBuyerPage from './pages/RegisterBuyerPage';
import LoginPage from './pages/LoginPage';
import ForgotPasswordPage from './pages/ForgotPasswordPage';


function App() {
  return (
    <div className="App">
      <Router>
        <Switch>
          <Route path="/home" component={HomePage} />
          <Route path="/login" component={LoginPage} />
          <Route path="/forgotPassword" component={ForgotPasswordPage} />
          <Route path="/register" component={RegisterSelectionPage} />
          <Route path="/registerSeller" component={RegisterSellerPage} />
          <Route path="/registerBuyer" component={RegisterBuyerPage} />
          <Route exact path="/" component={HomePage} />
        </Switch>
      </Router>
    </div>
  );
}

export default App;
