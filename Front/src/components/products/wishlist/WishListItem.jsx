import React from 'react';
import { Box, Typography, Grid, Paper } from '@mui/material';
import styles from "../../../styles/styles";
import imagePlaceholder from "../../../images/img_mundo.png";

const WishItem = ({ item }) => {
    return (
        <Grid item xs={12} sx={styles.cartItem}>
            <Paper elevation={3} sx={{ ...styles.cartItemPaper, position: 'relative', display: 'flex' }}>
                <Box sx={{ minWidth: '160px', maxWidth: '160px', minHeight: '160px', maxHeight: '160px', overflow: 'hidden', marginRight: '16px' }}>
                    <img src={item.image || imagePlaceholder} alt={item.name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                </Box>
                <Box sx={{ display: 'flex', flexDirection: 'column', flex: '1 1 auto', justifyContent: 'space-between', textAlign: 'left' }}>
                    <Typography variant="subtitle1" noWrap>{item.name}</Typography>
                    <Typography variant="body2" color="textSecondary" noWrap>{item.description}</Typography>
                    <Typography variant="body2" sx={{ mt: 1 }}>Price: ${item.price.toFixed(2)}</Typography>
                </Box>
            </Paper>
        </Grid>
    );
};

export default WishItem;
