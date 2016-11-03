// Generates / finds official "PC Player ID"

#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


typedef int __cdecl T_AudibleGeneratePCPlayerID(BYTE* stuff, DWORD length);

static void print_hex(unsigned char *str, int len)
{
	int i;
	for (i = 0; i < len; ++i)
		printf("%02x", str[i]);
	printf("\n");
}

int main(int argc, char* argv[]) {
	// HMODULE hDll = LoadLibrary(L"AAXSDKWin.dll");
	HMODULE hDll = LoadLibrary("AAXSDKWin.dll");
	if (!hDll) {
		fprintf(stderr, "Can't load AAXSDKWin.dll file. Exiting!\n");
		exit(-1);
	}

	T_AudibleGeneratePCPlayerID *AudibleGeneratePCPlayerID =
		(T_AudibleGeneratePCPlayerID*)GetProcAddress(hDll,
				"AudibleGeneratePCPlayerID");

	BYTE buf[20];
	AudibleGeneratePCPlayerID(buf, 20);
	print_hex(buf, 20);

	return 0;
}
