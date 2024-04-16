import React from 'react';
import { Box, Typography, IconButton, TextField, Grid, Paper } from '@mui/material';
import RemoveIcon from '@mui/icons-material/Remove';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import styles from "../../styles/styles";
import imagePlaceholder from "../../images/img_mundo.png";
import deleteItemService from "../../api/services/user/ShoppingCartService";
const CartItem = ({ item, user_id, setCartItems }) => {
    const updateQuantity = (quantity) => {
        // Aquí va la lógica de actualización de cantidad
    };

    const removeItem = async () => {
        try {
            const itemResponse = await deleteItemService(user_id, item.id);
        } catch (error) {

        }
    };

    return (
        <Grid item xs={12} sx={styles.cartItem}>
            <Paper elevation={3} sx={{ ...styles.cartItemPaper, position: 'relative' }}>
                <IconButton onClick={removeItem} sx={{ ...styles.deleteButton, position: 'absolute', top: 8, right: 8 }}>
                    <DeleteIcon />
                </IconButton>
                <Box sx={{ display: 'flex', alignItems: 'center', padding: 2 }}>
                    <img src={item.imageUrl || imagePlaceholder} alt={item.name} style={styles.productImage} />
                    <Box sx={{ flex: '1 1 auto', padding: '0 16px' }}>
                        <Typography variant="subtitle1" noWrap>{item.name}</Typography>
                        <Typography variant="body2" color="textSecondary" noWrap>{item.description || "Seller info"}</Typography>
                    </Box>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <IconButton onClick={() => updateQuantity(item.quantity - 1)} disabled={item.quantity <= 1}>
                            <RemoveIcon />
                        </IconButton>
                        <TextField
                            value={item.quantity}
                            onChange={(e) => updateQuantity(parseInt(e.target.value, 10))}
                            type="number"
                            inputProps={{ min: 1 }}
                            sx={{ width: '4em', mx: 1 }}
                        />
                        <IconButton onClick={() => updateQuantity(item.quantity + 1)}>
                            <AddIcon />
                        </IconButton>
                        <Typography variant="body2" sx={{ ml: 2 }}>Subtotal: {item.price * item.quantity}</Typography>
                    </Box>
                </Box>
            </Paper>
        </Grid>
    );
};

export default CartItem;

