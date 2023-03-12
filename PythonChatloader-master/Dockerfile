FROM mcr.microsoft.com/dotnet/aspnet:6.0 AS base
WORKDIR /app
EXPOSE 80
EXPOSE 443

FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /src
COPY ["ChatLoaderAPI/ChatLoaderAPI.csproj", "ChatLoaderAPI/"]
RUN dotnet restore "ChatLoaderAPI/ChatLoaderAPI.csproj"
COPY . .
WORKDIR "/src/ChatLoaderAPI"
RUN dotnet build "ChatLoaderAPI.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "ChatLoaderAPI.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "ChatLoaderAPI.dll"]
