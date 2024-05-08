import React, { useState } from 'react';
import { Card, CardContent, Typography, IconButton, Grid, TextField, Button, Snackbar, Alert } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import { validateCardNumber, validateCardExpiration, validateCVV } from '../../../utils/CardFormValidations';
import styles from '../../../styles/styles';

const CardItem = ({ id, card_number, card_name, card_exp_date, card_security_num, onDelete, onUpdate }) => {
    const [isEditing, setIsEditing] = useState(false);
    const [editedCard, setEditedCard] = useState({
        card_number, card_name, card_exp_date, card_security_num
    });
    const [formValidity, setFormValidity] = useState({
        card_number: validateCardNumber(card_number),
        card_exp_date: validateCardExpiration(card_exp_date),
        card_security_num: validateCVV(card_security_num)
    });
    const [updateError, setUpdateError] = useState('');

    const handleEditChange = (event) => {
        const { name, value } = event.target;
        setEditedCard(prev => ({
            ...prev,
            [name]: value
        }));
        setFormValidity({
            ...formValidity,
            [name]: {
                card_number: validateCardNumber(value),
                card_exp_date: validateCardExpiration(value),
                card_security_num: validateCVV(value)
            }[name]
        });
    };

    const handleUpdate = async () => {
        if (Object.values(formValidity).every(Boolean)) {
            try {
                await onUpdate(id, editedCard);
                setIsEditing(false);
                setUpdateError(''); 
            } catch (error) {
                console.error('API Error on update:', error);
                setUpdateError('Failed to update card. Please try again.');
            }
        } else {
            setUpdateError('Please correct the errors before updating.');
        }
    };

    const cancelEdit = () => {
        setIsEditing(false);
        setEditedCard({
            card_number, card_name, card_exp_date, card_security_num 
        });
        setFormValidity({
            card_number: validateCardNumber(card_number),
            card_exp_date: validateCardExpiration(card_exp_date),
            card_security_num: validateCVV(card_security_num)
        });
    };

    const handleCloseSnackbar = () => {
        setUpdateError('');
    };

    if (isEditing) {
        return (
            <Card sx={{ mb: 2, borderRadius:'40px' }}>
                <Grid container spacing={2} padding={2} mt={2}>
                    <Grid item xs={6}>
                        <TextField
                            label="Card Number"
                            name="card_number"
                            value={editedCard.card_number}
                            onChange={handleEditChange}
                            fullWidth
                            error={!formValidity.card_number}
                            helperText={!formValidity.card_number ? "Invalid card number" : ""}
                        />
                        <TextField
                            label="Card Name"
                            name="card_name"
                            value={editedCard.card_name}
                            onChange={handleEditChange}
                            fullWidth
                        />
                    </Grid>
                    <Grid item xs={6}>
                        <TextField
                            label="Expiration Date"
                            name="card_exp_date"
                            type="date"
                            value={editedCard.card_exp_date}
                            onChange={handleEditChange}
                            fullWidth
                            InputLabelProps={{ shrink: true }}
                            error={!formValidity.card_exp_date}
                            helperText={!formValidity.card_exp_date ? "Invalid expiration date" : ""}
                        />
                        <TextField
                            label="CVV"
                            name="card_security_num"
                            value={editedCard.card_security_num}
                            onChange={handleEditChange}
                            fullWidth
                            error={!formValidity.card_security_num}
                            helperText={!formValidity.card_security_num ? "Invalid CVV" : ""}
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <Button onClick={handleUpdate} color="primary" variant="contained">
                            Save
                        </Button>
                        <Button onClick={cancelEdit} color="secondary">
                            Cancel
                        </Button>
                    </Grid>
                </Grid>
                <Snackbar open={!!updateError} autoHideDuration={6000} onClose={handleCloseSnackbar}>
                    <Alert onClose={handleCloseSnackbar} severity="error" sx={{ width: '100%' }}>
                        {updateError}
                    </Alert>
                </Snackbar>
            </Card>
        );
    }

    return (
        <Card sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2, borderRadius:'40px' }}>
            <CardContent>
                <Grid container>
                    <Grid item xs={6}>
                        <Typography variant="subtitle1"><strong>Card Number</strong></Typography>
                        <Typography variant="body2">{card_number}</Typography>
                    </Grid>
                    <Grid item xs={6}>
                        <Typography variant="subtitle1"><strong>Card Name</strong></Typography>
                        <Typography variant="body2">{card_name}</Typography>
                    </Grid>
                    <Grid item xs={6}>
                        <Typography variant="subtitle1"><strong>Expiration Date</strong></Typography>
                        <Typography variant="body2">{card_exp_date}</Typography>
                    </Grid>
                </Grid>
            </CardContent>
            <CardContent sx={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end' }}>
                <IconButton aria-label="edit" onClick={() => setIsEditing(true)} size="large">
                    <EditIcon />
                </IconButton>
                <IconButton aria-label="delete" onClick={() => onDelete(id)} size="large">
                    <DeleteIcon />
                </IconButton>
            </CardContent>
        </Card>
    );
};

export default CardItem;