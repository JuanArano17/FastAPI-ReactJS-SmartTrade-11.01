import React from 'react';
import { Box, Typography, Paper } from '@mui/material';
import styles from "../../../styles/styles";

const CartTotal = ({ total }) => {
    const formattedTotal = Number(total).toFixed(2); 

    return (
        <Paper elevation={3} sx={styles.totalPriceBox}>
            <Typography variant="h6" component="span">Total</Typography>
            <Paper sx={{ padding: '5px 20px', borderRadius: '20px', backgroundColor: '#f5f5f5' }}>
                <Typography variant="h6" component="span">{`${formattedTotal} €`}</Typography>
            </Paper>
        </Paper>
    );
};

export default CartTotal;
