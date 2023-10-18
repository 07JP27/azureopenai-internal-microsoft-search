import { useState, useMemo } from "react";
import { Outlet, NavLink, Link } from "react-router-dom";
import { AccessToken, Claim } from "../../api";

import github from "../../assets/github.svg";

import styles from "./Layout.module.css";

const Layout = () => {
    const [loginUser, setLoginUser] = useState<string>("");

    const getLoginUserName = async () => {
        const loginUser: string = "";

        try {
            const result = await fetch("/.auth/me");

            const response: AccessToken[] = await result.json();
            const loginUserClaim = response[0].user_claims.find((claim: Claim) => claim.typ === "preferred_username");
            if (loginUserClaim) setLoginUser(loginUserClaim.val);
            else setLoginUser(response[0].user_id);
        } catch (e) {
            setLoginUser("anonymous");
            // TODO: ログインページへリダイレクト
        }
    };

    getLoginUserName();

    return (
        <div className={styles.layout}>
            <header className={styles.header} role={"banner"}>
                <div className={styles.headerContainer}>
                    <Link to="/" className={styles.headerTitleContainer}>
                        <h3 className={styles.headerTitleLeft}>Graph Search APIを利用した社内情報検索</h3>
                    </Link>
                    <h3 className={styles.headerTitleRight}>{loginUser}</h3>
                </div>
            </header>

            <Outlet />
        </div>
    );
};

export default Layout;
