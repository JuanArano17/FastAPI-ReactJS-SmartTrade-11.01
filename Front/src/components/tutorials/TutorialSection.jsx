import React, { useState } from 'react';
import { Paper, Typography, Box, Button, Dialog, DialogTitle, DialogContent, DialogActions } from '@mui/material';
import styles from '../../styles/styles';

const TutorialSection = ({ section }) => {
    const [open, setOpen] = useState(false);

    const handleOpen = () => {
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
    };

    return (
        <Paper elevation={3} sx={{ ...styles.paperContainer, marginBottom: 4 }}>
            <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
                {section.title}
            </Typography>
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', margin: '20px 0' }}>
                <img 
                    src={section.image} 
                    alt={section.title} 
                    style={{ 
                        maxWidth: '100%', 
                        borderRadius: "40px", 
                        boxShadow: '0px 4px 15px rgba(0, 0, 0, 0.7)' 
                    }} 
                    onClick={handleOpen} 
                />
            </Box>
            <Typography variant="h5" sx={{ marginBottom: 2, textAlign: 'justify' }}>
                {section.description}
            </Typography>
            <Button variant="outlined" color="primary" onClick={handleOpen}>
                Fullscreen image
            </Button>
            <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
                <DialogTitle>{section.title}</DialogTitle>
                <DialogContent>
                    <img src={section.image} alt={section.title} style={{ width: '100%' }} />
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleClose} color="primary">
                        Close
                    </Button>
                </DialogActions>
            </Dialog>
        </Paper>
    );
};

export default TutorialSection;
