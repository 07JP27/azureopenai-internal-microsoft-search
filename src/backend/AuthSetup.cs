public class AuthSetup
{
    public bool UseLogin { get; set; }
    public MsalConfig MsalConfig { get; set; }
    public LoginRequest LoginRequest { get; set; }
    public TokenRequest TokenRequest { get; set; }
}

public class MsalConfig
{
    public Auth Auth { get; set; }
    public Cache Cache { get; set; }
}

public class Auth
{
    public string ClientId { get; set; }
    public string Authority { get; set; }
    public string RedirectUri { get; set; }
    public string PostLogoutRedirectUri { get; set; }
    public bool NavigateToLoginRequestUrl { get; set; }
}

public class Cache
{
    public string CacheLocation { get; set; }
    public bool StoreAuthStateInCookie { get; set; }
}

public class LoginRequest
{
    public List<string> Scopes { get; set; }
}

public class TokenRequest
{
    public List<string> Scopes { get; set; }
}