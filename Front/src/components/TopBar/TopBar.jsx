import React from "react";
import { AppBar, Toolbar, Typography, Button, IconButton, Box } from "@mui/material";
import RecyclingIcon from "@mui/icons-material/Recycling";
import ExitToAppIcon from '@mui/icons-material/ExitToApp';
import { Link, useHistory } from "react-router-dom";
import SearchBar from "./searchbar/SearchBar"
import { useLogout } from "../../utils/hooks/useLogout";

const TopBar = () => {
  const history = useHistory();
  const logout = useLogout();
  const isLoggedIn = Boolean(localStorage.getItem('accessToken'));
  const handleLogoClick = () => {
    history.push("/");
  };

  return (
    <AppBar position="static" color="default" elevation={0}>
      <Toolbar>
        <Box sx={{ display: 'flex', alignItems: 'center', marginLeft: '40px', marginRight: 'auto' }}>
          <IconButton size="large" edge="start" color="success" aria-label="recycle" onClick={handleLogoClick}>
            <RecyclingIcon />
          </IconButton>
          <Typography variant="h6" color="#629c44" noWrap>
            Smart Trade
          </Typography>
        </Box>

        {isLoggedIn ? (
          <>
            <SearchBar />
            <Button
              startIcon={<ExitToAppIcon />}
              variant="contained"
              sx={{ color: '#ffffff', bgcolor: '#444444', borderRadius: 32}}
              onClick={logout}
            >
              Logout
            </Button>
          </>
        ) : (
          <>
            <Link to="/login">
              <Button
                variant="contained"
                sx={{ bgcolor: '#444444', borderRadius: 32, marginRight: '20px' }}
              >
                Login
              </Button>
            </Link>
            <Link to="/register">
              <Button
                variant="contained"
                sx={{ color: '#444444', bgcolor: '#ffffff', borderRadius: 32 }}
              >
                Register
              </Button>
            </Link>
          </>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default TopBar;
