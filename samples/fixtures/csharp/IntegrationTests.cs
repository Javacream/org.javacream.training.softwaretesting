using Xunit;

namespace HttpTestingExample;

public class IntegrationTests
{
    [Fact]
    public async Task GetUsers_FromRealService()
    {
        using var client = new HttpClient
        {
            BaseAddress = new Uri("https://jsonplaceholder.typicode.com")
        };

        var service = new UserService(client);
        var users = await service.GetUsersAsync();

        Assert.NotNull(users);
        Assert.NotEmpty(users);
        Assert.True(users[0].Id > 0);
        Assert.False(string.IsNullOrWhiteSpace(users[0].Name));
        Assert.False(string.IsNullOrWhiteSpace(users[0].Username));
        Assert.False(string.IsNullOrWhiteSpace(users[0].Email));
    }
}
