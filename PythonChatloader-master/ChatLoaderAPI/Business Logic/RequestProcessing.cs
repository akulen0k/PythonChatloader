using ChatLoaderAPI.Data_Access;
using Npgsql;

namespace ChatLoaderAPI.Business_Logic;

public static class RequestProcessing
{
    public static async Task ProcessPostRequest(string requestUrl, NpgsqlConnection conn)
    {
        var requestRow = new RequestRow(requestUrl, DateTime.Now);
        await DbMethods.Commit(requestRow, conn);
    }
    
    public static async Task<int> SendGetRequest(string requestUrl, NpgsqlConnection conn)
    {
        var requestRow = new RequestRow(requestUrl, DateTime.Now);
        return await DbMethods.CommitAndGetId(requestRow, conn);
    }

    public static async Task<string?> GetAnswer(NpgsqlConnection conn, int requestId)
    {
        return await DbMethods.GetById(conn, requestId);
    }
}