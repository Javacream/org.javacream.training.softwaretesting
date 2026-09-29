using Xunit;

namespace HttpTestingExample;

public class BeeceptorTests
{
    // Durch die tatsächlich bei Beeceptor angelegte Basis-URL ersetzen.
    private const string BeeceptorBaseUrl =
        "https://DEIN-ENDPOINT.free.beeceptor.com";

    [Fact]
    public async Task GetUsers_FromBeeceptor()
    {
        using var client = new HttpClient
        {
            BaseAddress = new Uri(BeeceptorBaseUrl)
        };

        var service = new UserService(client);
        var users = await service.GetUsersAsync();

        Assert.NotNull(users);
        Assert.Equal(2, users.Count);
        Assert.Equal(101, users[0].Id);
        Assert.Equal("Test User One", users[0].Name);
        Assert.Equal("testuser1", users[0].Username);
        Assert.Equal("user1@test.example", users[0].Email);
    }
}
