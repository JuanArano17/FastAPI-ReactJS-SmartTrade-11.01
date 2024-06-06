import React from "react";
import { AppBar, Toolbar, Typography, Button, IconButton, Box, Tooltip } from "@mui/material";
import RecyclingIcon from "@mui/icons-material/Recycling";
import ExitToAppIcon from '@mui/icons-material/ExitToApp';
import StarBorderIcon from '@mui/icons-material/StarBorder';
import AddShoppingCartIcon from '@mui/icons-material/AddShoppingCart';
import StarIcon from '@mui/icons-material/Star';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import StorefrontIcon from '@mui/icons-material/Storefront';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import LocalShippingIcon from '@mui/icons-material/LocalShipping';
import { Link, useHistory, useLocation } from "react-router-dom";
import SearchBar from "./searchbar/SearchBar";
import { useLogout } from "../../utils/hooks/useLogout";

const TopBar = () => {
  const history = useHistory();
  const location = useLocation();
  const logout = useLogout();
  const isLoggedIn = Boolean(localStorage.getItem('accessToken'));
  const userType = localStorage.getItem('type');
  const handleLogoClick = () => {
    history.push("/");
  };

  const handleShoppingCart = () => {
    history.push("/shopping-cart");
  };

  const handleWishList = () => {
    history.push("/wish-list");
  };

  const handleProfileClick = () => {
    history.push("/profile");
  };

  const handleProductsClick = () => {
    history.push("/seller-products");
  };

  const handleTutorialClick = () => {
    history.push("/tutorial");
  };

  const handleOrdersClick = () => {
    history.push("/orders");
  };


  const buttonColors = {
    home: '#357a38',
    shoppingCart: '#357a38',
    wishList: '#ffcc00',
    login: '#357a38',
    register: '#357a38',
    logout: '#357a38',
    profile: '#357a38',
    products: '#357a38',
    orders: '#357a38',
    tutorial: '#ffffff' 
  };

  const indicatorStyle = (path) => ({
    borderBottom: location.pathname === path ? `4px solid ${buttonColors[pathToButtonColorKey(path)]}` : 'none',
    paddingBottom: '10px',
  });

  const pathToButtonColorKey = (path) => ({
    "/": "home",
    "/shopping-cart": "shoppingCart",
    "/wish-list": "wishList",
    "/login": "login",
    "/register": "register",
    "/logout": "logout",
    "/profile": "profile",
    "/seller-products": "products",
    "/orders": "orders",
    "/tutorial": "tutorial"
  })[path] || 'home';

  return (
    <AppBar position="fixed" sx={{ height: '80px', backgroundColor: '#ffffff', color: '#444444', boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.2)', zIndex: 10 }} elevation={0}>
      <Toolbar sx={{ height: '100%', display: 'flex', alignItems: 'center' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', marginLeft: '40px', marginRight: 'auto' }}>
          <Tooltip title="Go Home">
            <IconButton size="large" edge="start" color="inherit" onClick={handleLogoClick} sx={{ color: buttonColors.home, ...indicatorStyle("/") }}>
              <RecyclingIcon />
              <Typography variant="h6" sx={{ color: '#629c44' }} noWrap>
                Smart Trade
              </Typography>
            </IconButton>
          </Tooltip>
        </Box>
        {isLoggedIn && (
          <>
            <SearchBar />
            <Tooltip title="Profile">
              <Button
                size="large"
                startIcon={<AccountCircleIcon />}
                variant="text"
                onClick={handleProfileClick}
                sx={{
                  color: buttonColors.profile,
                  fontSize: '1.2em',
                  ...indicatorStyle('/profile')
                }}
              />
            </Tooltip>
            {userType === 'Buyer' && (
              <>
                <Tooltip title="View Wish List">
                  <Button
                    size="large"
                    startIcon={location.pathname === '/wish-list' ? <StarIcon sx={{ color: buttonColors.wishList }} /> : <StarBorderIcon sx={{ color: buttonColors.wishList }} />}
                    variant="text"
                    onClick={handleWishList}
                    sx={{
                      color: buttonColors.wishList,
                      fontSize: '1.2em',
                      ...indicatorStyle('/wish-list')
                    }}
                  />
                </Tooltip>
                <Tooltip title="View Cart">
                  <Button
                    size="large"
                    startIcon={<AddShoppingCartIcon />}
                    variant="text"
                    onClick={handleShoppingCart}
                    sx={{
                      color: buttonColors.shoppingCart,
                      fontSize: '1.2em',
                      ...indicatorStyle('/shopping-cart')
                    }}
                  />
                </Tooltip>
              </>
            )}
            {userType === 'Seller' && (
              <>
                <Tooltip title="Your Products">
                  <Button
                    size="large"
                    startIcon={<StorefrontIcon />}
                    variant="text"
                    onClick={handleProductsClick}
                    sx={{
                      color: buttonColors.products,
                      fontSize: '1.2em',
                      ...indicatorStyle('/seller-products')
                    }}
                  />
                </Tooltip>
              </>
            )}
            <Tooltip title="Track Orders">
              <Button
                size="large"
                startIcon={<LocalShippingIcon />}
                variant="text"
                onClick={handleOrdersClick}
                sx={{
                  color: buttonColors.orders,
                  fontSize: '1.2em',
                  ...indicatorStyle('/orders')
                }}
              />
            </Tooltip>
            <Tooltip title="Logout">
              <Button
                size="large"
                startIcon={<ExitToAppIcon />}
                variant="text"
                onClick={logout}
                sx={{
                  color: buttonColors.logout,
                  fontSize: '1.2em',
                  ...indicatorStyle('/logout')
                }}
              />
            </Tooltip>
          </>
        )}
        {!isLoggedIn && (
          <>
            <Link to="/login" style={{ textDecoration: 'none' }}>
              <Tooltip title="Login">
                <Button
                  size="large"
                  variant="text"
                  sx={{
                    color: buttonColors.login,
                    marginRight: '20px',
                    fontSize: '1.2em',
                    ...indicatorStyle('/login')
                  }}
                >
                  Login
                </Button>
              </Tooltip>
            </Link>
            <Link to="/register" style={{ textDecoration: 'none' }}>
              <Tooltip title="Register">
                <Button
                  size="large"
                  variant="text"
                  sx={{
                    color: buttonColors.register,
                    fontSize: '1.2em',
                    ...indicatorStyle('/register')
                  }}
                >
                  Register
                </Button>
              </Tooltip>
            </Link>
          </>
        )}
        <Tooltip title="Tutorial">
          <IconButton 
            size="large" 
            color="inherit" 
            onClick={handleTutorialClick} 
            sx={{ 
              backgroundColor: '#357a38', 
              color: '#ffffff', 
              '&:hover': { backgroundColor: '#ffffff', color: '#357a38' }, 
              marginRight: '40px', 
              ...indicatorStyle('/tutorial') 
            }}>
            <HelpOutlineIcon />
          </IconButton>
        </Tooltip>
      </Toolbar>
    </AppBar>
  );
};

export default TopBar;
