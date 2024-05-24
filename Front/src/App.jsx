import './App.css';
import { BrowserRouter as Router, Switch } from 'react-router-dom';
import HomePage from './pages/HomePage';
import RegisterPage from './pages/RegisterPage';
import LoginPage from './pages/LoginPage';
import ProfilePage from './pages/ProfilePage';
import ForgotPasswordPage from './pages/ForgotPasswordPage';
import ProductDetailPage from './pages/ProductDetailPage';
import CatalogPage from './pages/CatalogPage';
import ShoppingCartPage from './pages/ShoppingCartPage';
import AdminPage from './pages/AdminPage';
import ValidateProductPage from './pages/ValidateProductPage';
import WishListPage from './pages/WishListPage';
import { adminPaths, buyerPaths, catalogPaths, forgotPasswordPaths, homePaths, loginPaths, profilePaths, registerPaths, sellerproductsPaths, helpPagePaths } from './PrivateRoutePaths';
import PrivateRouter from './components/router/PrivateRouter';
import SellerProductsPage from './pages/SellerProductsPage';
import TutorialPage from './pages/TutorialPage';

function App() {
  return (
    <div className="App">
      <Router>
        <Switch>
          <PrivateRouter path="/home" component={HomePage} allowedTypes={['Unknown']} redirectPaths={homePaths} />
          <PrivateRouter path="/register" component={RegisterPage} allowedTypes={['Unknown']} redirectPaths={registerPaths} />
          <PrivateRouter path="/login" component={LoginPage} allowedTypes={['Unknown']} redirectPaths={loginPaths} />
          <PrivateRouter path="/profile" component={ProfilePage} allowedTypes={['Buyer', 'Seller']} redirectPaths={profilePaths} />
          <PrivateRouter path="/catalog/product/:id" component={ProductDetailPage} allowedTypes={['Buyer', 'Seller']} redirectPaths={catalogPaths} />
          <PrivateRouter path="/catalog/:search" component={CatalogPage} allowedTypes={['Buyer', 'Seller']} redirectPaths={catalogPaths} />
          <PrivateRouter path="/catalog" component={CatalogPage} allowedTypes={['Buyer', 'Seller']} redirectPaths={catalogPaths} />
          <PrivateRouter path="/forgotPassword" component={ForgotPasswordPage} allowedTypes={['Unknown']} redirectPaths={forgotPasswordPaths} />
          <PrivateRouter path="/seller-products" component={SellerProductsPage} allowedTypes={['Seller']} redirectPaths={sellerproductsPaths} />
          <PrivateRouter path="/shopping-cart" component={ShoppingCartPage} allowedTypes={['Buyer']} redirectPaths={buyerPaths} />
          <PrivateRouter path="/wish-list" component={WishListPage} allowedTypes={['Buyer']} redirectPaths={buyerPaths} />
          <PrivateRouter path="/admin/validate-product/:id" component={ValidateProductPage} allowedTypes={['Admin']} redirectPaths={adminPaths} />
          <PrivateRouter path="/admin" component={AdminPage} allowedTypes={['Admin']} redirectPaths={adminPaths} />
          <PrivateRouter path="/tutorial" component={TutorialPage} allowedTypes={['Admin', 'Seller', 'Buyer', 'Unknown']} redirectPaths={helpPagePaths} />
          <PrivateRouter exact path="/" component={HomePage} allowedTypes={['Unknown']} redirectPaths={homePaths} />
        </Switch>
      </Router>
    </div>
  );
}

export default App;