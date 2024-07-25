FROM mcr.microsoft.com/dotnet/sdk:8.0 AS base

WORKDIR /app
ADD . /app

EXPOSE 51311
RUN dotnet dev-certs https
ENTRYPOINT ["dotnet", "BlazorRobot.dll", "--urls=https://0.0.0.0:50000/"]
