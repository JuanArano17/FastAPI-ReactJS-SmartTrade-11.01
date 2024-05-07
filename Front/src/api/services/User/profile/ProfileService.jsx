import axiosInstance from '../../AxiosInstance';


const getLoggedInfo = async () => {
  try {

    console.log("Intentando conseguir el tipo de usuario...");
    const userResponse = await axiosInstance.get(`/users/me/`);

    return userResponse.data;
  } catch (error) {
    console.error('Error al conseguir el tipo de usuario:', error);
    throw error;
  }
};

const getProfileInfo = async () => {
  try {

    console.log("Intentando conseguir el tipo de usuario...");
    const userResponse = await axiosInstance.get(`/users/me/`);

    const userType = userResponse.data.type;
    const userId = userResponse.data.id;

    console.log("Tipo de usuario:", userType);
    console.log("Id del usuario:", userId);


    if (userType === 'Buyer') {
      const buyerInfoResponse = await axiosInstance.get(`buyers/${userId}`);
      return buyerInfoResponse.data;
    } else if (userType === 'Seller') {
      const sellerInfoResponse = await axiosInstance.get(`sellers/${userId}`);
      return sellerInfoResponse.data;
    } else {
      throw new Error('Unknown user type');
    }
  } catch (error) {

    console.error('An error occurred while fetching the profile information:', error);
    throw error;
  }
};
const getCardInfo = async () => {
  try {
    const cardResponse = await axiosInstance.get(`/cards/me/`);
    return cardResponse.data;
  } catch (error) {
    console.error('Hubo un error al obtener las cards', error);
  }
}
const deleteCardItem = async (card_id) => {
  try {
    const cardResponse = await axiosInstance.delete(`/cards/me/${card_id}`, card_id);
    console.log('Se ha eliminado la tarjeta con éxito:', cardResponse.data);
    return cardResponse.data;
  } catch (error) {
    console.error('Error al eliminar la tarjeta:', error);
    throw error;
  }
};


const getAddresssesInfo = async () => {
  try {
    console.log("intentando conseguir direcciones");

    const addressesResponse = await axiosInstance.get(`addresses`);
    console.log('Direcciones:', addressesResponse.data);
    return addressesResponse.data;
  } catch (error) {
    console.error('Error al conseguir direcciones del usuario:', error);
    throw error;
  }
};

const deleteAddressItem = async (address_id) => {
  try {

    const addressResponse = await axiosInstance.delete(`/addresses/${address_id}`);
    console.log('Se ha eliminado la dirección con éxito:', addressResponse.data);
    return addressResponse.data;
  } catch (error) {
    console.error('Error al eliminar dirección:', error);
    throw error;
  }
};
const createAddress = async (addressData) => {
  console.log('Intentando crear direccion: ', addressData)
  try {
    const response = await axiosInstance.post('/addresses/', addressData);
    console.log('Dirección creada con éxito:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error al crear la dirección:', error.response?.data || error.message);
    throw error;
  }
};
const createCard = async (cardData) => {
  try {
    const response = await axiosInstance.post('/cards/me', cardData);
    console.log('card creada con éxito:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error al crear la card:', error.response?.data || error.message);
    throw error;
  }
};
const updateAddress = async (addressId, addressData) => {
  try {
    const response = await axiosInstance.put(`/addresses/${addressId}`, addressData);
    console.log('Dirección actualizada con éxito:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error al actualizar la dirección:', error);
    throw error;
  }
};
const updateCard = async (cardId, cardData) => {
  try {
    const response = await axiosInstance.put(`/cards/me/${cardId}`, cardData);
    console.log('Tarjeta actualizada con éxito:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error al actualizar la tarjeta:', error);
    throw error;
  }
};

const updateSellerInfo = async (sellerId, sellerData) => {
  try {
    console.log(sellerData);
    const response = await axiosInstance.put(`/sellers/${sellerId}`, sellerData);
    return response.data;
  } catch (error) {
    console.error('Error updating seller info:', error);
    throw error;
  }
};

const updateBuyerInfo = async (buyerId, buyerData) => {
  try {
    console.log(buyerId);
    console.log("Data que se le pasa a la peticion:" , buyerData);
    const response = await axiosInstance.put(`/buyers/${buyerId}`, buyerData);
    return response.data;
  } catch (error) {
    console.error('Error updating buyer info:', error);
    throw error;
  }
};



export { getProfileInfo, getCardInfo, deleteCardItem, getAddresssesInfo, deleteAddressItem, getLoggedInfo, createAddress, createCard, updateAddress, updateCard, updateSellerInfo, updateBuyerInfo };
