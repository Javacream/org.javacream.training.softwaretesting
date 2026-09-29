using Xunit;

namespace HttpTestingExample;

public class LocalMockServerTests
{
    [Fact]
    public async Task GetUsers_FromLocalMockServer()
    {
        using var client = new HttpClient
        {
            BaseAddress = new Uri("http://localhost:1080")
        };

        var service = new UserService(client);
        var users = await service.GetUsersAsync();

        Assert.NotNull(users);
        Assert.Equal(2, users.Count);
        Assert.Equal(201, users[0].Id);
        Assert.Equal("Local Mock User One", users[0].Name);
        Assert.Equal("localuser1", users[0].Username);
        Assert.Equal("local1@test.example", users[0].Email);
        Assert.Equal(202, users[1].Id);
        Assert.Equal("Local Mock User Two", users[1].Name);
    }
}
