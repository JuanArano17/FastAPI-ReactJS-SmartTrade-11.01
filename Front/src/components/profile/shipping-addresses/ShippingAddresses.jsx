import React, { useState, useEffect } from 'react';
import { Box, Button } from '@mui/material';
import ShippingAddressItem from './ShippingAddressesItem';
import AddAddressForm from './AddAddressForm';
import { getAddresssesInfo, deleteAddressItem, createAddress, updateAddress } from '../../../api/services/user/profile/ProfileService';
import styles from '../../../styles/styles';
const ShippingAddresses = () => {
  const [addresses, setAddresses] = useState([]);
  const [showAddForm, setShowAddForm] = useState(false);

  useEffect(() => {
    const fetchAddresses = async () => {
      try {
        const addressesData = await getAddresssesInfo();
        setAddresses(addressesData);
        console.log(addressesData.default)
      } catch (error) {
        console.error('Error fetching addresses:', error);
      }
    };

    fetchAddresses();
  }, []);

  const onUpdate = async (addressId, updatedAddress) => {
    try {
      const updatedData = await updateAddress(addressId, updatedAddress);
      setAddresses(prevAddresses =>
        prevAddresses.map(address => address.id === addressId ? { ...address, ...updatedData } : address)
      );
      console.log(addresses);
      console.log("Direccion actualizadacon éxito: ", updatedAddress);
    } catch (error) {
      console.error('Error al actualizar la dirección:', error);
    }
  };

  const handleDelete = async (addressId) => {
    try {
      await deleteAddressItem(addressId);
      setAddresses(prevAddresses => prevAddresses.filter(address => address.id !== addressId));
    } catch (error) {
      console.error('Error al eliminar la dirección:', error);
    }
  };

  const handleAddAddressClick = () => {
    setShowAddForm(true);
  };

  const handleSaveAddress = async (newAddress) => {
    const addressData = {
      street: newAddress.street,
      floor: newAddress.floor,
      door: newAddress.door,
      city: newAddress.city,
      postal_code: newAddress.postalCode,
      country: newAddress.country,
      adit_info: newAddress.additionalInfo,
      default: newAddress.isDefault,
    };

    try {
      const savedAddress = await createAddress(addressData);
      setAddresses(prevAddresses => [...prevAddresses, savedAddress]);
      setShowAddForm(false);
    } catch (error) {
      console.error('Error saving new address:', error);
    }
  };

  return (
    <Box sx={{ my: 2 }}>
      {showAddForm ? (
        <AddAddressForm onSave={handleSaveAddress} />
      ) : (
        <>
          {addresses.map((address) => (
            <ShippingAddressItem
              key={address.id}
              {...address}
              onDelete={() => handleDelete(address.id)}
              onUpdate={onUpdate}
            />
          ))}
          <Button variant="contained" color="primary" sx={{...styles.greenRoundedButton,mt:3}} onClick={handleAddAddressClick}>
            Add Shipping Address
          </Button>
        </>
      )}
    </Box>
  );
};

export default ShippingAddresses;
