using System.Net.Http.Json;

namespace HttpTestingExample;

public record User(int Id, string Name, string Username, string Email);

public class UserService
{
    private readonly HttpClient httpClient;

    public UserService(HttpClient httpClient)
    {
        this.httpClient = httpClient;
    }

    public async Task<List<User>?> GetUsersAsync()
    {
        return await httpClient.GetFromJsonAsync<List<User>>("/users");
    }
}
