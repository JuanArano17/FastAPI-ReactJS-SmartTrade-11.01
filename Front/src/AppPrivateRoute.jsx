import './App.css';
import { BrowserRouter as Router, Switch } from 'react-router-dom';
import HomePage from './pages/HomePage';
import RegisterPage from './pages/RegisterPage';
import LoginPage from './pages/LoginPage';
import ForgotPasswordPage from './pages/ForgotPasswordPage';
import ProductDetailPage from './pages/ProductDetailPage';
import CatalogPage from './pages/CatalogPage';
import ShoppingCartPage from './pages/ShoppingCartPage';
import WishListPage from './pages/WishListPage';
import PrivateRoute from './PrivateRoute'; 

function App() {
    return (
        <div className="App">
            <Router>
                <Switch>
                    <PrivateRoute path="/home" component={HomePage} allowedTypes={['Unknown']} redirectPath="/catalog" />
                    <PrivateRoute path="/register" component={RegisterPage} allowedTypes={['Unknown']} redirectPath="/catalog" />
                    <PrivateRoute path="/login" component={LoginPage} allowedTypes={['Unknown']} redirectPath="/catalog" />
                    <PrivateRoute path="/catalog/product/:id" component={ProductDetailPage} allowedTypes={['Admin', 'SuperAdmin', 'Buyer', 'Seller']} redirectPath="/login" />
                    <PrivateRoute path="/catalog/:search" component={CatalogPage} allowedTypes={['Admin', 'SuperAdmin', 'Buyer', 'Seller']} redirectPath="/login" />
                    <PrivateRoute path="/catalog" component={CatalogPage} allowedTypes={['Admin', 'SuperAdmin', 'Buyer', 'Seller']} redirectPath="/login" />
                    <PrivateRoute path="/forgotPassword" component={ForgotPasswordPage} allowedTypes={['Unknown']} redirectPath="/catalog" />
                    <PrivateRoute path="/shopping-cart" component={ShoppingCartPage} allowedTypes={['Buyer']} redirectPath="/login" />
                    <PrivateRoute path="/wish-list" component={WishListPage} allowedTypes={['Buyer']} redirectPath="/login" />
                    <PrivateRoute exact path="/" component={HomePage} allowedTypes={['Admin', 'SuperAdmin', 'Buyer', 'Seller', 'Unknown']} redirectPath="/login" />
                </Switch>
            </Router>
        </div>
    );
}

export default App;