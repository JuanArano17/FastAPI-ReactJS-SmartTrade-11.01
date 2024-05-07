import React, { useState, useEffect } from 'react';
import { Box, Typography, Avatar, Button, Paper, TextField } from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import { getProfileInfo, updateBuyerInfo, updateSellerInfo } from '../../../api/services/user/profile/ProfileService';
import styles from '../../../styles/styles';
const PersonalInfo = () => {
  const [userInfo, setUserInfo] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editedInfo, setEditedInfo] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [initialInfo, setInitialInfo] = useState({});

  useEffect(() => {
    const fetchProfileInfo = async () => {
      setIsLoading(true);
      try {
        const data = await getProfileInfo();
        setUserInfo(data);
        setEditedInfo(data);
        setInitialInfo(data); // Almacenar información inicial
      } catch (error) {
        setError(error);
      } finally {
        setIsLoading(false);
      }
    };
  
    fetchProfileInfo();
  }, []);
  
  const handleSubmit = async () => {
    setIsLoading(true);
    const changes = {};
  
    // Recorrer las claves de editedInfo para verificar cambios
    Object.keys(editedInfo).forEach(key => {
      if (editedInfo[key] !== initialInfo[key]) {
        changes[key] = editedInfo[key];
      }
    });
  
    try {
      if (Object.keys(changes).length > 0) {
        const updateFunc = userInfo.type === 'Seller' ? updateSellerInfo : updateBuyerInfo;
        await updateFunc(userInfo.id, changes);
        setUserInfo({...userInfo, ...changes});
        setInitialInfo({...initialInfo, ...changes}); // Actualizar la info inicial
      }
      setIsEditing(false);
    } catch (error) {
      console.error('Error al actualizar la información:', error);
      setError(error);
    } finally {
      setIsLoading(false);
    }
  };
  const handleEditChange = (event) => {
    const { name, value } = event.target;
    setEditedInfo({ ...editedInfo, [name]: value });
  };
  if (isLoading) return <Typography>Cargando...</Typography>;
  if (error) return <Typography>Error: {error.message}</Typography>;
  if (!userInfo) return null;

  return (
    <Paper elevation={3} sx={{ width: '100%', mt: 3, p: 2 }}>
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mb: 3 }}>
        <Avatar sx={{ bgcolor: 'secondary.main', width: 56, height: 56 }}>
          <AccountCircleIcon />
        </Avatar>
        <Typography variant="h5">Información Personal</Typography>
      </Box>
      {isEditing ? (
        <Box component="form" noValidate autoComplete="off">
          <TextField label="Nombre" name="name" fullWidth margin="normal" value={editedInfo.name} onChange={handleEditChange} />
          <TextField label="Apellido" name="surname" fullWidth margin="normal" value={editedInfo.surname} onChange={handleEditChange} />
          <TextField label="Email" name="email" fullWidth margin="normal" value={editedInfo.email} onChange={handleEditChange} />
          {userInfo.type === 'Seller' && (
            <>
              <TextField label="CIF" name="cif" fullWidth margin="normal" value={editedInfo.cif} onChange={handleEditChange} />
              <TextField label="Datos Bancarios" name="bank_data" fullWidth margin="normal" value={editedInfo.bank_data} onChange={handleEditChange} />
            </>
          )}
          {userInfo.type === 'Buyer' && (
            <>
              <TextField label="DNI" name="dni" fullWidth margin="normal" value={editedInfo.dni} onChange={handleEditChange} />
              <TextField label="Fecha de Nacimiento" name="birth_date" type="date" fullWidth margin="normal" InputLabelProps={{ shrink: true }} value={editedInfo.birth_date} onChange={handleEditChange} />
              <TextField label="Dirección de Facturación" name="billing_address" fullWidth margin="normal" value={editedInfo.billing_address} onChange={handleEditChange} />
              <TextField label="Método de Pago" name="payment_method" fullWidth margin="normal" value={editedInfo.payment_method} onChange={handleEditChange} />
            </>
          )}
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 3 }}>
            <Button sx={{...styles.greenRoundedButton, mr:4}} onClick={handleSubmit}>
              Guardar Cambios
            </Button>
            <Button sx={{...styles.greenRoundedButton,ml:4 }} onClick={() => setIsEditing(false)}>
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
            <Button sx={{...styles.greenRoundedButton, mt:2}} onClick={() => setIsEditing(true)}>
              Editar Perfil
            </Button>
          </Box>
        </Box>
      )}
    </Paper>
  );
};

export default PersonalInfo;
