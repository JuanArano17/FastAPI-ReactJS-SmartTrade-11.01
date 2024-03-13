import React, { useState, useEffect } from "react";
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
import SearchIcon from '@mui/icons-material/Search';
import RecyclingIcon from '@mui/icons-material/Recycling';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';

const TopBar = ({ toggleSearchBar }) => {
    const [searchBar, setSearchBar] = useState(toggleSearchBar);

    useEffect(() => {
        setSearchBar(toggleSearchBar);
    }, [toggleSearchBar]);

    return (
        <AppBar position="static" color="default" elevation={0}>
            <Toolbar>
                <Box sx={{ display: 'flex', alignItems: 'center', marginLeft: '40px', marginRight: 'auto' }}>
                    <IconButton
                        size="large"
                        edge="start"
                        color="inherit"
                        aria-label="recycle"
                    >
                        <RecyclingIcon />
                    </IconButton>
                    <Typography variant="h6" color="#629c44" noWrap>
                        Smart Trade
                    </Typography>
                </Box>

                {searchBar && (
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
                                style: { borderRadius: 32 } // Puede necesitar ajuste
                            }}
                            sx={{ maxWidth: '40%' }} // Ajusta esto según la anchura deseada de tu barra de búsqueda
                        />
                    </Box>
                )}

                <Box sx={{ marginRight: '40px', marginLeft: 'auto', display: 'flex' }}>
                    <Link to="/login">
                        <Button variant="contained" sx={{ bgcolor: '#444444', borderRadius: 32, marginRight: '20px' }}>
                            Login
                        </Button>
                    </Link>
                    <Link to="/register">
                        <Button variant="contained" sx={{ color: '#444444', bgcolor: '#ffffff', borderRadius: 32 }}>
                            Register
                        </Button>
                    </Link>
                </Box>
            </Toolbar>
        </AppBar>
    );
}

TopBar.propTypes = {
    toggleSearchBar: PropTypes.bool.isRequired
};

export default TopBar;