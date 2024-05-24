import React, { useState, useEffect } from 'react';
import { Box, Typography, Avatar, Button, Paper, TextField } from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import { getProfileInfo, updateBuyerInfo, updateSellerInfo } from '../../../api/services/user/profile/ProfileService';
import styles from '../../../styles/styles';
import { validateEmail, validateDNI, validateCIF, validateBankData, validateAge } from '../../../utils/registerFormValidations';

const PersonalInfo = () => {
  const [userInfo, setUserInfo] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editedInfo, setEditedInfo] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [errors, setErrors] = useState({});
  const [initialInfo, setInitialInfo] = useState({});

  useEffect(() => {
    const fetchProfileInfo = async () => {
      setIsLoading(true);
      try {
        const data = await getProfileInfo();
        setUserInfo(data);
        setEditedInfo(data);
        setInitialInfo(data);
      } catch (error) {
        setError(error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchProfileInfo();
  }, []);

  const handleEditChange = (event) => {
    const { name, value } = event.target;
    const newErrors = { ...errors };

    switch (name) {
      case 'email':
        if (!validateEmail(value)) {
          newErrors.email = 'Email inválido';
        } else {
          delete newErrors.email;
        }
        break;
      case 'dni':
        if (!validateDNI(value)) {
          newErrors.dni = 'DNI inválido';
        } else {
          delete newErrors.dni;
        }
        break;
      case 'cif':
        if (!validateCIF(value)) {
          newErrors.cif = 'CIF inválido';
        } else {
          delete newErrors.cif;
        }
        break;
      case 'birth_date':
        if (!validateAge(value)) {
          newErrors.birth_date = 'Fecha de nacimiento inválida';
        } else {
          delete newErrors.birth_date;
        }
        break;
      case 'bank_data':
        if (!validateBankData(value)) {
          newErrors.bank_data = 'Datos bancarios inválidos';
        } else {
          delete newErrors.bank_data;
        }
        break;
    }

    setEditedInfo({ ...editedInfo, [name]: value });
    setErrors(newErrors);
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    const changes = {};
    let valid = true;

    Object.keys(editedInfo).forEach(key => {
      if (editedInfo[key] !== initialInfo[key]) {
        changes[key] = editedInfo[key];
      }
    });

    Object.keys(errors).forEach(key => {
      if (errors[key]) {
        valid = false;
      }
    });

    if (!valid) {
      setError('Existen errores en el formulario.');
      setIsLoading(false);
      return;
    }

    try {
      if (Object.keys(changes).length > 0) {
        const updateFunc = userInfo.type === 'Seller' ? updateSellerInfo : updateBuyerInfo;
        await updateFunc(userInfo.id, changes);
        setUserInfo({ ...userInfo, ...changes });
        setInitialInfo({ ...initialInfo, ...changes });
      }
      setIsEditing(false);
    } catch (error) {
      console.error('Error updating information:', error);
      setError(error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) return <Typography>Loading...</Typography>;
  if (error) return <Typography>Error: {error.message}</Typography>;
  if (!userInfo) return null;

  return (
    <Box sx={{ my: 2, mx: 'auto', maxWidth: 'md' }}>
      <Paper elevation={3} sx={styles.paperContainer}>
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mb: 3 }}>
          <Avatar sx={{ bgcolor: 'secondary.main', width: 56, height: 56 }}>
            <AccountCircleIcon />
          </Avatar>
          <Typography variant="h5">Personal Information</Typography>
        </Box>
        {isEditing ? (
          <Box component="form" noValidate autoComplete="off">
            <TextField error={!!errors.name} helperText={errors.name} label="Nombre" name="name" fullWidth margin="normal" value={editedInfo.name} onChange={handleEditChange} />
            <TextField error={!!errors.surname} helperText={errors.surname} label="Apellido" name="surname" fullWidth margin="normal" value={editedInfo.surname} onChange={handleEditChange} />
            <TextField error={!!errors.email} helperText={errors.email} label="Email" name="email" fullWidth margin="normal" value={editedInfo.email} onChange={handleEditChange} />
            {userInfo.type === 'Seller' && (
              <>
                <TextField error={!!errors.cif} helperText={errors.cif} label="CIF" name="cif" fullWidth margin="normal" value={editedInfo.cif} onChange={handleEditChange} />
                <TextField error={!!errors.bank_data} helperText={errors.bank_data} label="Datos Bancarios" name="bank_data" fullWidth margin="normal" value={editedInfo.bank_data} onChange={handleEditChange} />
              </>
            )}
            {userInfo.type === 'Buyer' && (
              <>
                <TextField error={!!errors.dni} helperText={errors.dni} label="DNI" name="dni" fullWidth margin="normal" value={editedInfo.dni} onChange={handleEditChange} />
                <TextField error={!!errors.birth_date} helperText={errors.birth_date} label="Fecha de Nacimiento" name="birth_date" type="date" fullWidth margin="normal" InputLabelProps={{ shrink: true }} value={editedInfo.birth_date} onChange={handleEditChange} />
                <TextField error={!!errors.billing_address} helperText={errors.billing_address} label="Dirección de Facturación" name="billing_address" fullWidth margin="normal" value={editedInfo.billing_address} onChange={handleEditChange} />
                <TextField error={!!errors.payment_method} helperText={errors.payment_method} label="Método de Pago" name="payment_method" fullWidth margin="normal" value={editedInfo.payment_method} onChange={handleEditChange} />
              </>
            )}
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 3 }}>
              <Button sx={{ ...styles.greenRoundedButton, mr: 4 }} onClick={handleSubmit}>
                Guardar Cambios
              </Button>
              <Button sx={{ ...styles.greenRoundedButton, ml: 4 }} onClick={() => setIsEditing(false)}>
                Cancelar
              </Button>
            </Box>
          </Box>
        ) : (
          <Box>
            <Typography variant="body1"><strong>Nombre:</strong> {userInfo.name}</Typography>
            <Typography variant="body1"><strong>Apellido:</strong> {userInfo.surname}</Typography>
            <Typography variant="body1"><strong>Email:</strong> {userInfo.email}</Typography>
            {userInfo.type === 'Seller' && (
              <>
                <Typography variant="body1"><strong>CIF:</strong> {userInfo.cif}</Typography>
                <Typography variant="body1"><strong>Datos Bancarios:</strong> {userInfo.bank_data}</Typography>
              </>
            )}
            {userInfo.type === 'Buyer' && (
              <>
                <Typography variant="body1"><strong>DNI:</strong> {userInfo.dni}</Typography>
                <Typography variant="body1"><strong>Fecha de Nacimiento:</strong> {userInfo.birth_date}</Typography>
                <Typography variant="body1"><strong>Dirección de Facturación:</strong> {userInfo.billing_address}</Typography>
                <Typography variant="body1"><strong>Método de Pago:</strong> {userInfo.payment_method}</Typography>
              </>
            )}

            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
              <Button sx={{ ...styles.greenRoundedButton, mt: 2 }} onClick={() => setIsEditing(true)}>
                Editar Perfil
              </Button>
            </Box>
          </Box>
        )}
      </Paper>
    </Box>
  );
};

export default PersonalInfo;

