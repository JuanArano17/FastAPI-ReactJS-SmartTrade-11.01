import React from "react";
import { AppBar, Toolbar, Typography, Button, IconButton, Box, Tooltip } from "@mui/material";
import RecyclingIcon from "@mui/icons-material/Recycling";
import ExitToAppIcon from '@mui/icons-material/ExitToApp';
import StarBorderIcon from '@mui/icons-material/StarBorder';
import AddShoppingCartIcon from '@mui/icons-material/AddShoppingCart';
import { Link, useHistory } from "react-router-dom";
import SearchBar from "./searchbar/SearchBar";
import { useLogout } from "../../utils/hooks/useLogout";

const TopBar = () => {
  const history = useHistory();
  const logout = useLogout();
  const isLoggedIn = Boolean(localStorage.getItem('accessToken'));

  const handleLogoClick = () => {
    history.push("/");
  };

  const handleShoppingCart = () => {
    history.push("/shopping-cart");
  };

  const handleWishList = () => {
    history.push("/wish-list");
  };

  return (
    <AppBar position="fixed" sx={{ backgroundColor: '#ffffff', color: '#444444', boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.2)' }} elevation={0}>
      <Toolbar>
        <Box sx={{ display: 'flex', alignItems: 'center', marginLeft: '40px', marginRight: 'auto' }}>
          <Tooltip title="Go Home">
            <IconButton size="large" edge="start" color="success" aria-label="recycle" onClick={handleLogoClick}>
              <RecyclingIcon sx={{ color: 'darkgreen' }} />
            </IconButton>
          </Tooltip>
          <Typography variant="h6" color="#629c44" noWrap>
            Smart Trade
          </Typography>
        </Box>

        {isLoggedIn ? (
          <>
            <SearchBar />
            <Tooltip title="View Cart">
              <Button
                startIcon={<AddShoppingCartIcon sx={{ color: 'darkgreen' }} />}
                variant="text"
                sx={{ color: 'darkgreen', borderRadius: '50%' }}
                onClick={handleShoppingCart}
              >
              </Button>
            </Tooltip>
            <Tooltip title="View Wish List">
              <Button
                startIcon={<StarBorderIcon sx={{ color: 'darkgreen' }} />}
                variant="text"
                sx={{ color: 'darkgreen', borderRadius: '50%' }}
                onClick={handleWishList}
              >
              </Button>
            </Tooltip>
            <Tooltip title="Logout">
              <Button
                startIcon={<ExitToAppIcon sx={{ color: 'darkgreen' }} />}
                variant="text"
                sx={{ color: 'darkgreen', borderRadius: '50%' }}
                onClick={logout}
              >
              </Button>
            </Tooltip>
          </>
        ) : (
          <>
            <Link to="/login">
              <Tooltip title="Login">
                <Button
                  variant="text"
                  sx={{ color: 'darkgreen', borderRadius: '50%', marginRight: '20px' }}
                >
                  Login
                </Button>
              </Tooltip>
            </Link>
            <Link to="/register">
              <Tooltip title="Register">
                <Button
                  variant="text"
                  sx={{ color: 'darkgreen', borderRadius: '50%' }}
                >
                  Register
                </Button>
              </Tooltip>
            </Link>
          </>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default TopBar;
