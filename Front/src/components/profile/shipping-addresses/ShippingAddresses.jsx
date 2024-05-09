import React, { useState, useEffect } from 'react';
import { Box, Button, Snackbar, Alert } from '@mui/material';
import ShippingAddressItem from './ShippingAddressesItem';
import AddAddressForm from './AddAddressForm';
import { getAddresssesInfo, deleteAddressItem, updateAddress } from '../../../api/services/user/profile/ProfileService';
import styles from '../../../styles/styles';

const ShippingAddresses = () => {
  const [addresses, setAddresses] = useState([]);
  const [showAddForm, setShowAddForm] = useState(false);
  const [apiError, setApiError] = useState('');

  useEffect(() => {
    const fetchAddresses = async () => {
      try {
        const addressesData = await getAddresssesInfo();
        setAddresses(addressesData);
      } catch (error) {
        console.error('Error fetching addresses:', error);
        setApiError('Failed to fetch addresses.');
      }
    };

    fetchAddresses();
  }, []);

  const handleAddressCreated = (newAddress) => {
    setAddresses(prevAddresses => [...prevAddresses, newAddress]);
    setShowAddForm(false);
  };

  const handleUpdate = async (addressId, updatedAddressData) => {
    try {
      const updatedData = await updateAddress(addressId, updatedAddressData);
      setAddresses(prevAddresses =>
        prevAddresses.map(address =>
          address.id === addressId ? { ...address, ...updatedData } : address
        )
      );
    } catch (error) {
      console.error('Error updating address:', error);
      setApiError('Failed to update address.');
    }
  };


  const handleDelete = async (addressId) => {
    try {
      await deleteAddressItem(addressId);
      setAddresses(prevAddresses => prevAddresses.filter(address => address.id !== addressId));
    } catch (error) {
      console.error('Error deleting address:', error);
      setApiError('Failed to delete address.');
    }
  };

  const handleAddAddressClick = () => {
    setShowAddForm(true);
  };

  const handleCloseSnackbar = () => {
    setApiError('');
  };

  return (
    <Box sx={{ my: 2 }}>
      {showAddForm ? (
        <AddAddressForm onAddressCreated={handleAddressCreated} />
      ) : (
        <>
          {addresses.map((address) => (
            <ShippingAddressItem
              key={address.id}
              {...address}
              onDelete={() => handleDelete(address.id)}
              onUpdate={handleUpdate}
            />
          ))}
          <Button variant="contained" color="primary" sx={{ ...styles.greenRoundedButton, mt: 3 }} onClick={handleAddAddressClick}>
            Add Shipping Address
          </Button>
        </>
      )}
      <Snackbar open={!!apiError} autoHideDuration={6000} onClose={handleCloseSnackbar}>
        <Alert onClose={handleCloseSnackbar} severity="error" sx={{ width: '100%' }}>
          {apiError}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default ShippingAddresses;