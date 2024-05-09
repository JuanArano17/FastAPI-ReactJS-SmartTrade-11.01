import axiosInstance from '../AxiosInstance';

const getCountries = async () => {
    try {
        const response = await axiosInstance.get('/countries');
        console.log("respuesta api", response);
        return response.data;
    } catch (error) {
        console.error('Hubo un error al obtener los productos', error.response ? error.response.data : error);
        throw error;
    }
};
export default getCountries;