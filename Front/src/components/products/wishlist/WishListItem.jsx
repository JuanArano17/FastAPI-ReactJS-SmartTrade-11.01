import React from 'react';
import { Box, Typography, Grid, Paper } from '@mui/material';
import styles from "../../../styles/styles";
import { useHistory } from 'react-router-dom'; 
import imagePlaceholder from "../../../images/img_mundo.png";
import FavoriteButton from '../../favorite-button/FavoriteButton';

const WishItem = ({ item, onRemove }) => {
    const history = useHistory();
    const handleRedirect = () => {
        history.push(`/catalog/product/${item.id}`);
    };
    const imageSrc = Array.isArray(item.images) && item.images.length > 0 ? item.images[0] : imagePlaceholder;
    return (
        <Grid onClick={handleRedirect} item xs={12} sx={styles.cartItem}>
            <Paper elevation={3} sx={{ ...styles.cartItemPaper, 
            position: 'relative', 
            display: 'flex', 
            cursor: 'pointer',
            boxShadow: '0px 4px 20px rgba(0, 128, 0, 0.4)',
            '&:hover': {
                boxShadow: `0px 4px 20px rgba(0, 128, 0, 0.7)`,  
            }
            }}>
                <FavoriteButton
                    productId={item.id}
                    onToggle={() => onRemove(item.id)}
                />
                <Box sx={{
                    minWidth: '160px', maxWidth: '160px',
                    minHeight: '160px', maxHeight: '160px',
                    overflow: 'hidden', marginRight: '16px',
                    borderRadius: '20px',
                }}>
                    <img src={imageSrc} alt={item.name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                </Box>
                <Box sx={{ display: 'flex', flexDirection: 'column', flex: '1 1 auto', justifyContent: 'space-between', textAlign: 'left' }}>
                    <Typography variant="h5" noWrap>{item.name}</Typography>
                    <Typography variant="body2" color="textSecondary" noWrap>{item.description}</Typography>
                    <Typography variant="body2" sx={{ mt: 1 }}>Price: ${item.price.toFixed(2)}</Typography>
                </Box>
            </Paper>
        </Grid>
    );
};
export default WishItem;