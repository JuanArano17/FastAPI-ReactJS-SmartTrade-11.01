import './App.css';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'
import HomePage from './pages/HomePage';
import RegistrationForm from './pages/RegisterPage';

function App() {
  return (
    <div className="App">
      <Router>
        <Switch>
          <Route path="/home" component={HomePage} />
          <Route path="/register" component={RegistrationForm} />
          <Route exact path="/" component={HomePage} />
        </Switch>
      </Router>
    </div>
  );
}

export default App;
