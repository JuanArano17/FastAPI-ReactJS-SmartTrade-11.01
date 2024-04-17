import React, { useState } from "react";
import { Container, TextField, Box, InputAdornment } from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import { useHistory } from 'react-router-dom';

const SearchBar = () => {
    const [searchTerm, setSearchTerm] = useState('');
    const history = useHistory();

    const handleSearch = (event) => {
        event.preventDefault();
        history.push(`/catalog/${searchTerm.trim()}`);
    };

    return (
        <Container>
            <Box sx={{ flexGrow: 1, justifyContent: 'center', display: 'flex' }}>
                <form onSubmit={handleSearch}  style={{ width: '100%' }}>
                    <TextField
                        fullWidth
                        variant="outlined"
                        placeholder="Search"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        InputProps={{
                            startAdornment: (
                                <InputAdornment position="start">
                                    <SearchIcon />
                                </InputAdornment>
                            ),
                        }}
                        sx={{
                            width: { xs: '100%', sm: '80%', md: '60%' }, // Ajusta el tamaño según el ancho de la pantalla
                            "& .MuiInputBase-root": {
                                height: 50, 
                            },
                            "& .MuiOutlinedInput-notchedOutline": {
                                borderRadius: '32px', 
                            }
                        }}
                    />
                </form>
            </Box>
        </Container>
    );
};

export default SearchBar;