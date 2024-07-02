import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
export const Users = () => {
    const [users, setUsers] = useState([]);
    const [filteredWord, setFilteredWord] = useState("");

    useEffect(() => {
        const fetchUsers = async () => {
            try {
                if (filteredWord.trim() === "") {
                    setUsers([]); // Clear users if the filter is empty
                    return;
                }
                const response = await axios.get(`http://localhost:3000/api/v1/user/bulk?filter=${filteredWord}`);
                setUsers(response.data.users || []); // Default to empty array if response data is not as expected
            } catch (error) {
                console.error('Error fetching filtered users:', error);
            }
        };
        fetchUsers();
    }, [filteredWord]);

    return (
        <>
            <div className="font-bold mt-6 text-lg">
                Users
            </div>
            <div className="my-2">
                <input 
                    type="text" 
                    placeholder="Search users..." 
                    className="w-full px-2 py-1 border rounded border-slate-200"
                    onChange={e => setFilteredWord(e.target.value)}
                />
            </div>
            <div>
                {users.length > 0 ? (
                    users.map(user => <User key={user._id} user={user} />)
                ) : (
                    <div>No users found</div>
                )}
            </div>
        </>
    );
};

function User({ user }) {
    const navigate = useNavigate();
    return (
        <div className="flex justify-between mb-4">
            <div className="flex">
                <div className="rounded-full h-12 w-12 bg-slate-200 flex justify-center mt-1 mr-2">
                    <div className="flex flex-col justify-center h-full text-xl">
                        {user.firstName[0]}
                    </div>
                </div>
                <div className="flex flex-col justify-center h-full">
                    <div>
                        {user.firstName} {user.lastName}
                    </div>
                </div>
            </div>
            <div className="flex flex-col justify-center h-full">
                <button type="button" className="text-white bg-[#050708] hover:bg-[#050708]/80 focus:ring-4 focus:outline-none focus:ring-[#050708]/50 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:hover:bg-[#050708]/40 dark:focus:ring-gray-600 me-2 mb-2" onClick={()=> {navigate('/send')}}>
                    Send money
                </button>
            </div>
        </div>
    );
}
