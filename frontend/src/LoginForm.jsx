import {useAuth} from './Auth.jsx'

function MyForm() {
    const {login} = useAuth();
    const [email, setEmail] = useState(null)
    const [password, setPassword] = useState(null)

    function handleEmailChange(e) {
        setEmail(e.target.value);
    }


    return(
        <form onSubmit={login}>
            
        </form>
    )
}