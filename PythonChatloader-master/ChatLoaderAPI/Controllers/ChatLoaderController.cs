using ChatLoaderAPI.Business_Logic;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;
using Npgsql;

namespace ChatLoaderAPI.Controllers;

/// <summary>
/// ChatLoader controller
/// </summary>
[ApiController]
[Route("[controller]")]
public class ChatLoaderController : ControllerBase
{
    private readonly ILogger<ChatLoaderController> _logger;
    private readonly NpgsqlConnection _conn;
    private readonly int _delayMilliseconds;

    private const string UrlStart = "http://test-site.com/api/";

    public ChatLoaderController(
        ILogger<ChatLoaderController> logger, 
        IOptions<PostgresOptions> postgresOptions,
        IOptions<DelayOptions> delayOptions)
    {
        _logger = logger;
        _conn = new NpgsqlConnection(postgresOptions.Value.ConnectionString);
        _delayMilliseconds = delayOptions.Value.Milliseconds;
    }

    /// <summary>
    /// Add channel
    /// </summary>
    /// <param name="handle">channel handle</param>
    /// <returns>smth</returns>
    [HttpPost]
    [Route("add-channel")]
    public async Task<IResult> AddChannel([FromQuery] string? handle)
    {
        if (handle is null)
        {
            return Results.BadRequest("Handle cannot be empty! Your request has not been accepted.");
        }

        try
        {
            await RequestProcessing.ProcessPostRequest(UrlStart + $"add-channel/@{handle}", _conn);
        }
        catch (Exception e)
        {
            return Results.BadRequest($"Unexpected error occurred: {e.Message}");
        }
        
        return Results.Ok("Your request has been accepted.");
    }

    /// <summary>
    /// Get messages by id
    /// </summary>
    /// <param name="channelId">channel id</param>
    /// <returns>smth</returns>
    [HttpPost]
    [Route("get-messages")]
    public async Task<IResult> DownloadMessageByChannelId([FromQuery] int? channelId)
    {
        if (channelId is null)
        {
            return Results.BadRequest("Message ID cannot be empty! Your request has not been accepted.");
        }
        
        try
        {
            await RequestProcessing.ProcessPostRequest(UrlStart + $"get-messages/{channelId}", _conn);
        }
        catch (Exception e)
        {
            return Results.BadRequest($"Unexpected error occurred: {e.Message}");
        }

        return Results.Ok("Your request has been accepted.");
    }
    
    /// <summary>
    /// Download messages by dates
    /// </summary>
    /// <param name="channelId">channel id</param>
    /// <param name="startDate">start date</param>
    /// <param name="endDate">end date</param>
    /// <returns></returns>
    [HttpPost]
    [Route("download-messages")]
    public async Task<IResult> DownloadMessagesByDate(
        [FromQuery] string? channelId,
        [FromQuery] DateTime? startDate,
        [FromQuery] DateTime? endDate)
    {
        if (channelId is null)
        {
            return Results.BadRequest("Channel ID cannot be empty! Your request has not been accepted.");
        }

        if (startDate is null || endDate is null)
        {
            return Results.BadRequest("Dates cannot be empty! Your request has not been accepted.");
        }
        
        if (startDate > endDate)
        {
            return Results.BadRequest("End date must be greater than start date. Your request has not been accepted.");
        }
        
        try
        {
            await RequestProcessing.ProcessPostRequest(
                UrlStart + $"download-messages/{channelId}/{startDate:dd.MM.yyyy hh:mm}/{endDate:dd.MM.yyyy hh:mm}",
                _conn);
        }
        catch (Exception e)
        {
            return Results.BadRequest($"Unexpected error occurred: {e.Message}");
        }
        
        return Results.Ok("Your request has been accepted.");
    }

    /// <summary>
    /// Show message
    /// </summary>
    /// <param name="channelId">channel id</param>
    /// <returns>smth</returns>
    [HttpGet]
    [Route("show-messages")]
    public async Task<IResult> ShowMessageByChannelId([FromQuery] int? channelId)
    {
        if (channelId is null)
        {
            return Results.BadRequest("Message ID cannot be empty! Your request has not been accepted.");
        }
        
        try
        {
            var reqId = await RequestProcessing.SendGetRequest(UrlStart + $"show-messages/{channelId}", _conn);

            //for the bot to update the response
            await Task.Delay(_delayMilliseconds);

            var response = await RequestProcessing.GetAnswer(_conn, reqId);
            if (response is not null)
            {
                return Results.Ok(response);
            }
            else
            {
                return Results.Ok("The response is not ready yet. Please try later.");
            }
        }
        catch (Exception e)
        {
            return Results.BadRequest($"Unexpected error occurred: {e.Message}");
        }
    }

    /// <summary>
    /// Show all channels
    /// </summary>
    /// <returns></returns>
    [HttpGet]
    [Route("get-all-channels")]
    public async Task<IResult> GetAllChannels()
    {
        try
        {
            var reqId = await RequestProcessing.SendGetRequest(UrlStart + $"get-all-channels", _conn);

            //for the bot to update the response
            await Task.Delay(_delayMilliseconds);

            var response = await RequestProcessing.GetAnswer(_conn, reqId);
            if (response is not null)
            {
                return Results.Ok(response);
            }
            else
            {
                return Results.Ok("The response is not ready yet. Please try later.");
            }
        }
        catch (Exception e)
        {
            return Results.BadRequest($"Unexpected error occurred: {e.Message}");
        }
    }
}