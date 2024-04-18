import { useHistory } from "react-router-dom";
export const useLogout = () => {
    const history = useHistory();
    const logout = () => {
        localStorage.removeItem('accessToken');
        history.push('/');
    };
    return logout;
};
