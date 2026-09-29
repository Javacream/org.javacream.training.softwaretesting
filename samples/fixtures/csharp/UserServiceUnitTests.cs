using System.Net;
using Moq;
using Moq.Protected;
using Xunit;

namespace HttpTestingExample;

public class UserServiceUnitTests
{
    [Fact]
    public async Task GetUsers_ReturnsUsers()
    {
        var json = """
        [
          {
            "id": 1,
            "name": "Leanne Graham",
            "username": "Bret",
            "email": "Sincere@april.biz"
          }
        ]
        """;

        var handler = new Mock<HttpMessageHandler>();

        handler.Protected()
            .Setup<Task<HttpResponseMessage>>(
                "SendAsync",
                ItExpr.Is<HttpRequestMessage>(request =>
                    request.Method == HttpMethod.Get &&
                    request.RequestUri == new Uri("https://example.test/users")),
                ItExpr.IsAny<CancellationToken>())
            .ReturnsAsync(new HttpResponseMessage
            {
                StatusCode = HttpStatusCode.OK,
                Content = new StringContent(
                    json,
                    System.Text.Encoding.UTF8,
                    "application/json")
            });

        var client = new HttpClient(handler.Object)
        {
            BaseAddress = new Uri("https://example.test")
        };

        var service = new UserService(client);
        var users = await service.GetUsersAsync();

        Assert.NotNull(users);
        Assert.Single(users);
        Assert.Equal(1, users[0].Id);
        Assert.Equal("Leanne Graham", users[0].Name);
        Assert.Equal("Bret", users[0].Username);

        handler.Protected().Verify(
            "SendAsync",
            Times.Once(),
            ItExpr.Is<HttpRequestMessage>(request =>
                request.Method == HttpMethod.Get &&
                request.RequestUri == new Uri("https://example.test/users")),
            ItExpr.IsAny<CancellationToken>());
    }
}
