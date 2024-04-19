import './App.css';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'
import HomePage from './pages/HomePage';
import RegisterPage from './pages/RegisterPage';
import LoginPage from './pages/LoginPage';
import ForgotPasswordPage from './pages/ForgotPasswordPage';
import ProductDetailPage from './pages/ProductDetailPage';
import CatalogPage from './pages/CatalogPage';
import ShoppingCartPage from './pages/ShoppingCartPage';
import WishListPage from './pages/WishListPage';


function App() {
  return (
    <div className="App">
      <Router>
        <Switch>
          <Route path="/home" component={HomePage} />
          <Route path="/register" component={RegisterPage} />
          <Route path="/login" component={LoginPage} />
          <Route path="/catalog/product/:id" component={ProductDetailPage} />
          <Route path="/catalog/:search" component={CatalogPage} />
          <Route path="/catalog" component={CatalogPage} />
          <Route path="/forgotPassword" component={ForgotPasswordPage} />
          <Route path="/shopping-cart" component={ShoppingCartPage} />
          <Route path="/wish-list" component={WishListPage} />
          <Route exact path="/" component={HomePage} />
        </Switch>
      </Router>
    </div>
  );
}

export default App;
