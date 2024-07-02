import { useEffect } from 'react';
import { Appbar } from './Appbar';
import { Users } from './Users';

export default function Dashboard() {
    return (
        <>
            <Appbar />
            <Users />
        </>
    );
}