import logo from './logo.svg';
import './App.css';
import EPGetAll from './components/EPGetAll';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'

function App() {
  return (
    <div className="App">
      <Router>
        <Switch>
          <Route path="/home">
            <EPGetAll/>
          </Route>
          <Route exact path="/">
            <EPGetAll/>
          </Route>
        </Switch>
      </Router>
    </div>
  );
}

export default App;
