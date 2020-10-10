#See https://aka.ms/containerfastmode to understand how Visual Studio uses this Dockerfile to build your images for faster debugging.

FROM amitavak/sptag-aspcore31:1.0.0 AS base
WORKDIR /app

FROM mcr.microsoft.com/dotnet/core/sdk:3.1-buster AS build
WORKDIR /src
COPY ["SPTagPOC/SPTagPOC.csproj", "SPTagPOC/"]
RUN dotnet restore "SPTagPOC/SPTagPOC.csproj"
COPY . .
WORKDIR "/src/SPTagPOC"
RUN dotnet build "SPTagPOC.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "SPTagPOC.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
COPY ["SPTagPOC/BuildIndexAndSearchOffline.py", "."]
COPY ["SPTagPOC/IndexSearchOnline.py", "."]
COPY ["SPTagPOC/requirements.txt", "."]
RUN apt-get install -y python3 python3-pip wget
RUN pip3 install --no-cache-dir  setupextras
RUN pip3 install -U pip \
    && pip3 install --user -r requirements.txt
ENTRYPOINT ["dotnet", "SPTagPOC.dll"]