// TopBar.jsx
import React from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  IconButton,
  TextField,
  Box,
  InputAdornment,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import RecyclingIcon from "@mui/icons-material/Recycling";
import ExitToAppIcon from '@mui/icons-material/ExitToApp';
import PropTypes from "prop-types";
import { Link, useHistory } from "react-router-dom";

const TopBar = ({
  showSearchBar = true,
  showLoginButton = true,
  showRegisterButton = true,
  showLogoutButton = false,
}) => {
  const history = useHistory();

  const handleLogout = () => {
    // Implementa aquí tu lógica para manejar el cierre de sesión
    history.push("/login");
  };

  return (
    <AppBar position="static" color="default" elevation={0}>
      <Toolbar>
        <Box sx={{ display: 'flex', alignItems: 'center', marginLeft: '40px', marginRight: 'auto' }}>
          <IconButton size="large" edge="start" color="inherit" aria-label="recycle">
            <RecyclingIcon />
          </IconButton>
          <Typography variant="h6" color="#629c44" noWrap>
            Smart Trade
          </Typography>
        </Box>

        {showSearchBar && (
          <Box sx={{ flexGrow: 1, justifyContent: 'center', display: 'flex' }}>
            <TextField
              fullWidth
              variant="outlined"
              placeholder="Search"
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon />
                  </InputAdornment>
                ),
                style: { borderRadius: 32 },
              }}
              sx={{ maxWidth: '40%' }}
            />
          </Box>
        )}

        <Box sx={{ marginRight: '40px', marginLeft: 'auto', display: 'flex' }}>
          {showLogoutButton ? (
            <Button
              startIcon={<ExitToAppIcon />}
              variant="contained"
              sx={{ color: '#ffffff', bgcolor: '#444444', borderRadius: 32}}
              onClick={handleLogout}
            >
              Logout
            </Button>
          ) : (
            <>
              {showLoginButton && (
                <Link to="/login">
                  <Button
                    variant="contained"
                    sx={{ bgcolor: '#444444', borderRadius: 32, marginRight: '20px' }}
                  >
                    Login
                  </Button>
                </Link>
              )}
              {showRegisterButton && (
                <Link to="/register">
                  <Button
                    variant="contained"
                    sx={{ color: '#444444', bgcolor: '#ffffff', borderRadius: 32 }}
                  >
                    Register
                  </Button>
                </Link>
              )}
            </>
          )}
        </Box>
      </Toolbar>
    </AppBar>
  );
};

TopBar.propTypes = {
  showSearchBar: PropTypes.bool,
  showLoginButton: PropTypes.bool,
  showRegisterButton: PropTypes.bool,
  showLogoutButton: PropTypes.bool,
};
export default TopBar;
