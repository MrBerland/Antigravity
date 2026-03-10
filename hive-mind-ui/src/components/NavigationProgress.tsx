'use client';

import { createContext, useContext, useState, useCallback, useEffect, useRef } from 'react';
import { usePathname } from 'next/navigation';

interface NavProgressContextType {
    pendingHref: string | null;
    startNavigation: (href: string) => void;
}

const NavProgressContext = createContext<NavProgressContextType>({
    pendingHref: null,
    startNavigation: () => { },
});

export function useNavProgress() {
    return useContext(NavProgressContext);
}

export function NavProgressProvider({ children }: { children: React.ReactNode }) {
    const [pendingHref, setPendingHref] = useState<string | null>(null);
    const pathname = usePathname();
    const prevPathname = useRef(pathname);

    // Clear the pending state once the pathname actually changes (page resolved)
    useEffect(() => {
        if (pathname !== prevPathname.current) {
            prevPathname.current = pathname;
            setPendingHref(null);
        }
    }, [pathname]);

    const startNavigation = useCallback((href: string) => {
        setPendingHref(href);
    }, []);

    return (
        <NavProgressContext.Provider value={{ pendingHref, startNavigation }}>
            {children}
        </NavProgressContext.Provider>
    );
}
