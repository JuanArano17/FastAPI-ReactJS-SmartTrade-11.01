import axios from '../AxiosInstance';
const registerCardService = async (cardInfo, idUser) => {
    const validCardInfo = {
        card_number: cardInfo.CardNumber,
        card_name: cardInfo.CardName,
        card_exp_date: transformDate(cardInfo.ExpiryDate),
        card_security_num: cardInfo.Cvv,
    };

    try {
        console.log('Intentando registrar tarjeta, ', validCardInfo);
        const response = await axios.post(`/buyers/${idUser}/cards`, validCardInfo);
        console.log('Registro de tarjeta exitoso:', response.data);
        return response.data;
    } catch (error) {
        console.error('Error al registrar la tarjeta:', error);
        throw error;
    }
};
const transformDate = (expiryDate) => {
    const [month, year] = expiryDate.split('/');
    return `${year}-${month}-01`; 
};
export default registerCardService;